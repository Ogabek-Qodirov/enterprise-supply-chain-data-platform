
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BRONZE_FILE = (
    PROJECT_ROOT / "data" / "bronze" / "wms_inventory.csv"
)

SILVER_WAREHOUSES = (
    PROJECT_ROOT / "data" / "silver" / "wms" / "warehouses.parquet"
)

SILVER_PRODUCTS = (
    PROJECT_ROOT / "data" / "silver" / "oms" / "products.parquet"
)

SILVER_DIR = PROJECT_ROOT / "data" / "silver" / "wms"
SILVER_FILE = SILVER_DIR / "inventory.parquet"


def transform_inventory():

    # 1. Bronze ma'lumotlarini o'qish
    df = pd.read_csv(BRONZE_FILE)

    # 2. Ustun nomlarini standartlashtirish
    df.columns = df.columns.str.strip().str.lower()

    # 3. Matn ustunlarini tozalash
    for column in ["warehouse_id", "product_id"]:
        df[column] = df[column].astype("string").str.strip()

    # 4. Majburiy qiymatlarni tekshirish
    required_columns = [
        "inventory_id",
        "warehouse_id",
        "product_id",
        "quantity",
        "last_updated_at"
    ]

    if df[required_columns].isna().any().any():
        raise ValueError("Majburiy qiymatlarda NULL aniqlandi.")

    # 5. Primary Key tekshiruvi
    if df["inventory_id"].duplicated().any():
        raise ValueError("Takrorlangan inventory_id aniqlandi.")

    # 6. Numeric formatga o'tkazish
    df["inventory_id"] = pd.to_numeric(
        df["inventory_id"],
        errors="raise"
    ).astype("int64")

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="raise"
    ).astype("int64")

    # 7. Business Rule tekshiruvi
    if (df["quantity"] < 0).any():
        raise ValueError("Inventory quantity manfiy bo'lishi mumkin emas.")

    # 8. Timestamp formatiga o'tkazish
    df["last_updated_at"] = pd.to_datetime(
        df["last_updated_at"],
        errors="raise"
    )

    # 9. Foreign Key tekshiruvlari
    warehouses = pd.read_parquet(SILVER_WAREHOUSES)
    products = pd.read_parquet(SILVER_PRODUCTS)

    valid_warehouse_ids = set(warehouses["warehouse_id"])
    valid_product_ids = set(products["product_id"])

    if not df["warehouse_id"].isin(valid_warehouse_ids).all():
        raise ValueError("Noto'g'ri warehouse_id aniqlandi.")

    if not df["product_id"].isin(valid_product_ids).all():
        raise ValueError("Noto'g'ri product_id aniqlandi.")

    # 10. Ombor + mahsulot kombinatsiyasini tekshirish
    if df.duplicated(
        subset=["warehouse_id", "product_id"]
    ).any():
        raise ValueError(
            "Bir omborda bir xil mahsulot uchun takroriy inventory mavjud."
        )

    # 11. Silver Layer'ga saqlash
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        SILVER_FILE,
        engine="pyarrow",
        index=False
    )

    print("INVENTORY SILVER TRANSFORMATION COMPLETED")
    print(f"Records: {len(df)}")
    print(f"Output: {SILVER_FILE}")


if __name__ == "__main__":
    transform_inventory()
