
from pathlib import Path
from decimal import Decimal

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

BRONZE_FILE = BASE_DIR / "data" / "bronze" / "finance_warehouse_expenses.csv"
SILVER_DIR = BASE_DIR / "data" / "silver" / "finance"
SILVER_FILE = SILVER_DIR / "warehouse_expenses.parquet"


def transform_warehouse_expenses():
    df = pd.read_csv(BRONZE_FILE)

    # 1. Matnli ustunlarni tozalash
    text_columns = [
        "warehouse_id",
        "expense_category",
        "description",
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # 2. Majburiy ustunlarni tekshirish
    required_columns = [
        "expense_id",
        "warehouse_id",
        "expense_category",
        "expense_amount",
        "expense_timestamp",
    ]

    if df[required_columns].isna().any().any():
        raise ValueError("Required columns contain NULL values.")

    # 3. Primary Key tekshiruvi
    if df["expense_id"].duplicated().any():
        raise ValueError("Duplicate expense_id values found.")

    df["expense_id"] = df["expense_id"].astype("int64")

    # 4. Foreign Key tekshiruvi
    warehouses_file = BASE_DIR / "data" / "silver" / "wms" / "warehouses.parquet"
    warehouses_df = pd.read_parquet(warehouses_file)

    valid_warehouse_ids = set(warehouses_df["warehouse_id"])

    invalid = df.loc[
        ~df["warehouse_id"].isin(valid_warehouse_ids),
        "warehouse_id"
    ]

    if not invalid.empty:
        raise ValueError(
            f"Invalid warehouse_id values: {invalid.tolist()}"
        )

    # 5. Pul qiymatlarini Decimal formatiga o'tkazish
    df["expense_amount"] = df["expense_amount"].map(
        lambda value: Decimal(str(value))
    )

    if (df["expense_amount"] < Decimal("0")).any():
        raise ValueError("Negative expense amounts found.")

    # 6. Sana ustunini datetime formatiga o'tkazish
    df["expense_timestamp"] = pd.to_datetime(
        df["expense_timestamp"],
        errors="raise"
    )

    # 7. Silver Layer'ga saqlash
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        SILVER_FILE,
        index=False,
        engine="pyarrow"
    )

    print("WAREHOUSE EXPENSES SILVER TRANSFORMATION COMPLETED")
    print(f"Records: {len(df)}")
    print(f"Output: {SILVER_FILE}")


if __name__ == "__main__":
    transform_warehouse_expenses()
