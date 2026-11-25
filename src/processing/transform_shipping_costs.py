
from pathlib import Path
from decimal import Decimal

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

BRONZE_FILE = BASE_DIR / "data" / "bronze" / "finance_shipping_costs.csv"
SILVER_DIR = BASE_DIR / "data" / "silver" / "finance"
SILVER_FILE = SILVER_DIR / "shipping_costs.parquet"


def transform_shipping_costs():
    df = pd.read_csv(BRONZE_FILE)

    # 1. Matnli ustunlarni tozalash
    text_columns = [
        "shipment_id",
        "description",
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # 2. Majburiy ustunlarni tekshirish
    required_columns = [
        "shipping_cost_id",
        "shipment_id",
        "shipping_amount",
        "recorded_at",
    ]

    if df[required_columns].isna().any().any():
        raise ValueError("Required columns contain NULL values.")

    # 3. Primary Key tekshiruvi
    if df["shipping_cost_id"].duplicated().any():
        raise ValueError("Duplicate shipping_cost_id values found.")

    df["shipping_cost_id"] = df["shipping_cost_id"].astype("int64")

    # 4. Foreign Key tekshiruvi
    shipments_file = BASE_DIR / "data" / "silver" / "tms" / "shipments.parquet"
    shipments_df = pd.read_parquet(shipments_file)

    valid_shipment_ids = set(shipments_df["shipment_id"])

    invalid = df.loc[
        ~df["shipment_id"].isin(valid_shipment_ids),
        "shipment_id"
    ]

    if not invalid.empty:
        raise ValueError(
            f"Invalid shipment_id values: {invalid.tolist()}"
        )

    # 5. Pul qiymatlarini Decimal formatiga o'tkazish
    df["shipping_amount"] = df["shipping_amount"].map(
        lambda value: Decimal(str(value))
    )

    if (df["shipping_amount"] < Decimal("0")).any():
        raise ValueError("Negative shipping amounts found.")

    # 6. Sana ustunini datetime formatiga o'tkazish
    df["recorded_at"] = pd.to_datetime(
        df["recorded_at"],
        errors="raise"
    )

    # 7. Silver Layer'ga saqlash
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        SILVER_FILE,
        index=False,
        engine="pyarrow"
    )

    print("SHIPPING COSTS SILVER TRANSFORMATION COMPLETED")
    print(f"Records: {len(df)}")
    print(f"Output: {SILVER_FILE}")


if __name__ == "__main__":
    transform_shipping_costs()
