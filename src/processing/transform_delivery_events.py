
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

BRONZE_FILE = BASE_DIR / "data" / "bronze" / "tms_delivery_events.csv"
SILVER_DIR = BASE_DIR / "data" / "silver" / "tms"
SILVER_FILE = SILVER_DIR / "delivery_events.parquet"


def transform_delivery_events():
    df = pd.read_csv(BRONZE_FILE)

    # 1. Matnli ustunlarni tozalash
    text_columns = [
        "shipment_id",
        "event_type",
        "event_location",
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # 2. Majburiy ustunlarni tekshirish
    required_columns = [
        "delivery_event_id",
        "shipment_id",
        "event_type",
        "event_timestamp",
        "ingested_at",
    ]

    if df[required_columns].isna().any().any():
        raise ValueError("Required columns contain NULL values.")

    # 3. Primary Key tekshiruvi
    if df["delivery_event_id"].duplicated().any():
        raise ValueError("Duplicate delivery_event_id values found.")

    df["delivery_event_id"] = df["delivery_event_id"].astype("int64")

    # 4. Foreign Key tekshiruvi
    parent_file = SILVER_DIR / "shipments.parquet"
    parent_df = pd.read_parquet(parent_file)

    valid_shipment_ids = set(parent_df["shipment_id"])

    invalid = df.loc[
        ~df["shipment_id"].isin(valid_shipment_ids),
        "shipment_id"
    ]

    if not invalid.empty:
        raise ValueError(
            f"Invalid shipment_id values: {invalid.tolist()}"
        )

    # 5. Vaqt ustunlarini datetime formatiga o'tkazish
    datetime_columns = [
        "event_timestamp",
        "ingested_at",
    ]

    for column in datetime_columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="raise"
        )

    # 6. Voqea vaqti ingestion vaqtidan oldin bo'lmasligi kerak
    if (df["ingested_at"] < df["event_timestamp"]).any():
        raise ValueError(
            "Some events were ingested before they occurred."
        )

    # 7. Natijani Parquet formatida saqlash
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        SILVER_FILE,
        index=False,
        engine="pyarrow"
    )

    print("DELIVERY EVENTS SILVER TRANSFORMATION COMPLETED")
    print(f"Records: {len(df)}")
    print(f"Output: {SILVER_FILE}")


if __name__ == "__main__":
    transform_delivery_events()
