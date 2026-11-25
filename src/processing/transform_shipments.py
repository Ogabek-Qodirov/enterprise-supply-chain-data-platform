
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

BRONZE_FILE = BASE_DIR / "data" / "bronze" / "tms_shipments.csv"
SILVER_DIR = BASE_DIR / "data" / "silver" / "tms"
SILVER_FILE = SILVER_DIR / "shipments.parquet"


def transform_shipments():
    df = pd.read_csv(BRONZE_FILE)

    # 1. Matnli ustunlarni tozalash
    text_columns = [
        "shipment_id",
        "order_id",
        "carrier_id",
        "warehouse_id",
        "shipment_status",
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # 2. Majburiy ustunlarni tekshirish
    required_columns = [
        "shipment_id",
        "order_id",
        "carrier_id",
        "warehouse_id",
        "required_handoff_at",
        "shipment_status",
    ]

    if df[required_columns].isna().any().any():
        raise ValueError("Required columns contain NULL values.")

    # 3. Primary Key tekshiruvi
    if df["shipment_id"].duplicated().any():
        raise ValueError("Duplicate shipment_id values found.")

    # 4. Foreign Key tekshiruvlari
    relationships = {
        "order_id": "oms/orders.parquet",
        "carrier_id": "tms/carriers.parquet",
        "warehouse_id": "wms/warehouses.parquet",
    }

    for column, relative_path in relationships.items():
        parent_file = BASE_DIR / "data" / "silver" / relative_path
        parent_df = pd.read_parquet(parent_file)

        valid_keys = set(parent_df[column.replace(
            "order_id", "order_id"
        ).replace(
            "carrier_id", "carrier_id"
        ).replace(
            "warehouse_id", "warehouse_id"
        )])

        invalid = df.loc[
            ~df[column].isin(valid_keys),
            column
        ]

        if not invalid.empty:
            raise ValueError(
                f"Invalid {column} values: {invalid.tolist()}"
            )

    # 5. Sana ustunlarini datetime formatiga o'tkazish
    datetime_columns = [
        "required_handoff_at",
        "actual_handoff_at",
        "expected_delivery_at",
        "actual_delivery_at",
    ]

    for column in datetime_columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="raise"
        )

    # 6. Bitta buyurtmaga bitta jo'natma
    if df["order_id"].duplicated().any():
        raise ValueError("Multiple shipments found for one order.")

    # 7. Silver Layer'ga saqlash
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        SILVER_FILE,
        index=False,
        engine="pyarrow"
    )

    print("SHIPMENTS SILVER TRANSFORMATION COMPLETED")
    print(f"Records: {len(df)}")
    print(f"Output: {SILVER_FILE}")


if __name__ == "__main__":
    transform_shipments()
