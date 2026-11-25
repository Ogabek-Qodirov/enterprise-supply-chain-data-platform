
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

BRONZE_FILE = BASE_DIR / "data" / "bronze" / "tms_carriers.csv"
SILVER_DIR = BASE_DIR / "data" / "silver" / "tms"
SILVER_FILE = SILVER_DIR / "carriers.parquet"


def transform_carriers():
    df = pd.read_csv(BRONZE_FILE)

    # 1. Matnli ustunlarni tozalash
    text_columns = [
        "carrier_id",
        "carrier_name",
        "service_type",
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # 2. Majburiy ustunlarni tekshirish
    required_columns = [
        "carrier_id",
        "carrier_name",
        "service_type",
        "created_at",
    ]

    if df[required_columns].isna().any().any():
        raise ValueError("Required columns contain NULL values.")

    # 3. Primary Key tekshiruvi
    if df["carrier_id"].duplicated().any():
        raise ValueError("Duplicate carrier_id values found.")

    # 4. Sana ustunini datetime formatiga o'tkazish
    df["created_at"] = pd.to_datetime(
        df["created_at"],
        errors="raise"
    )

    # 5. Natijani Parquet formatida saqlash
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        SILVER_FILE,
        index=False,
        engine="pyarrow"
    )

    print("CARRIERS SILVER TRANSFORMATION COMPLETED")
    print(f"Records: {len(df)}")
    print(f"Output: {SILVER_FILE}")


if __name__ == "__main__":
    transform_carriers()
