
from pathlib import Path
from decimal import Decimal

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

BRONZE_FILE = BASE_DIR / "data" / "bronze" / "finance_order_revenue.csv"
SILVER_DIR = BASE_DIR / "data" / "silver" / "finance"
SILVER_FILE = SILVER_DIR / "order_revenue.parquet"


def transform_order_revenue():
    df = pd.read_csv(BRONZE_FILE)

    # 1. Matnli ustunlarni tozalash
    df["order_id"] = df["order_id"].astype("string").str.strip()

    # 2. Majburiy ustunlarni tekshirish
    required_columns = [
        "revenue_id",
        "order_id",
        "revenue_amount",
        "recognized_at",
    ]

    if df[required_columns].isna().any().any():
        raise ValueError("Required columns contain NULL values.")

    # 3. Primary Key tekshiruvi
    if df["revenue_id"].duplicated().any():
        raise ValueError("Duplicate revenue_id values found.")

    df["revenue_id"] = df["revenue_id"].astype("int64")

    # 4. Foreign Key tekshiruvi
    orders_file = BASE_DIR / "data" / "silver" / "oms" / "orders.parquet"
    orders_df = pd.read_parquet(orders_file)

    valid_order_ids = set(orders_df["order_id"])

    invalid = df.loc[
        ~df["order_id"].isin(valid_order_ids),
        "order_id"
    ]

    if not invalid.empty:
        raise ValueError(f"Invalid order_id values: {invalid.tolist()}")

    # 5. Bitta buyurtma uchun bitta revenue yozuvi
    if df["order_id"].duplicated().any():
        raise ValueError("Multiple revenue records found for one order.")

    # 6. Moliyaviy qiymatlarni Decimal formatiga o'tkazish
    df["revenue_amount"] = df["revenue_amount"].map(
        lambda value: Decimal(str(value))
    )

    if (df["revenue_amount"] < Decimal("0")).any():
        raise ValueError("Negative revenue amounts found.")

    # 7. Sana ustunini datetime formatiga o'tkazish
    df["recognized_at"] = pd.to_datetime(
        df["recognized_at"],
        errors="raise"
    )

    # 8. Silver Layer'ga saqlash
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        SILVER_FILE,
        index=False,
        engine="pyarrow"
    )

    print("ORDER REVENUE SILVER TRANSFORMATION COMPLETED")
    print(f"Records: {len(df)}")
    print(f"Output: {SILVER_FILE}")


if __name__ == "__main__":
    transform_order_revenue()
