
import pandas as pd
from decimal import Decimal
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BRONZE_FILE = (
    PROJECT_ROOT / "data" / "bronze" / "oms_order_items.csv"
)

SILVER_ORDERS = (
    PROJECT_ROOT / "data" / "silver" / "oms" / "orders.parquet"
)

SILVER_PRODUCTS = (
    PROJECT_ROOT / "data" / "silver" / "oms" / "products.parquet"
)

SILVER_DIR = PROJECT_ROOT / "data" / "silver" / "oms"
SILVER_FILE = SILVER_DIR / "order_items.parquet"


def transform_order_items():

    # 1. Bronze ma'lumotlarini o'qish
    df = pd.read_csv(BRONZE_FILE)

    # 2. Ustun nomlarini standartlashtirish
    df.columns = df.columns.str.strip().str.lower()

    # 3. Matn ustunlarini tozalash
    for column in ["order_id", "product_id"]:
        df[column] = df[column].astype("string").str.strip()

    # 4. Majburiy qiymatlarni tekshirish
    required_columns = [
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price"
    ]

    if df[required_columns].isna().any().any():
        raise ValueError("Majburiy qiymatlarda NULL aniqlandi.")

    # 5. Primary Key tekshiruvi
    if df["order_item_id"].duplicated().any():
        raise ValueError("Takrorlangan order_item_id aniqlandi.")

    # 6. Numeric turlarni o'zgartirish
    df["order_item_id"] = pd.to_numeric(
        df["order_item_id"],
        errors="raise"
    ).astype("int64")

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="raise"
    ).astype("int64")

    df["unit_price"] = df["unit_price"].map(
        lambda value: Decimal(str(value))
    )

    # 7. Business rule tekshiruvlari
    if (df["quantity"] <= 0).any():
        raise ValueError("Quantity 0 dan katta bo'lishi kerak.")

    if (df["unit_price"] < Decimal("0")).any():
        raise ValueError("Unit price manfiy bo'lishi mumkin emas.")

    # 8. Foreign Key tekshiruvlari
    orders = pd.read_parquet(SILVER_ORDERS)
    products = pd.read_parquet(SILVER_PRODUCTS)

    valid_order_ids = set(orders["order_id"])
    valid_product_ids = set(products["product_id"])

    if not df["order_id"].isin(valid_order_ids).all():
        raise ValueError("Mavjud bo'lmagan order_id aniqlandi.")

    if not df["product_id"].isin(valid_product_ids).all():
        raise ValueError("Mavjud bo'lmagan product_id aniqlandi.")

    # 9. Silver formatida saqlash
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        SILVER_FILE,
        engine="pyarrow",
        index=False
    )

    print("ORDER ITEMS SILVER TRANSFORMATION COMPLETED")
    print(f"Records: {len(df)}")
    print(f"Output: {SILVER_FILE}")


if __name__ == "__main__":
    transform_order_items()
