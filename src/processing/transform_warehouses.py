
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BRONZE_FILE = (
    PROJECT_ROOT / "data" / "bronze" / "wms_warehouses.csv"
)

SILVER_DIR = PROJECT_ROOT / "data" / "silver" / "wms"
SILVER_FILE = SILVER_DIR / "warehouses.parquet"


def transform_warehouses():

    # 1. Bronze ma'lumotlarini o'qish
    df = pd.read_csv(BRONZE_FILE)

    # 2. Ustun nomlarini standartlashtirish
    df.columns = df.columns.str.strip().str.lower()

    # 3. Matn ustunlarini tozalash
    text_columns = [
        "warehouse_id",
        "warehouse_name",
        "city"
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # 4. Majburiy ustunlarni tekshirish
    required_columns = [
        "warehouse_id",
        "warehouse_name",
        "city",
        "warehouse_capacity"
    ]

    if df[required_columns].isna().any().any():
        raise ValueError("Majburiy qiymatlarda NULL aniqlandi.")

    # 5. Primary Key tekshiruvi
    if df["warehouse_id"].duplicated().any():
        raise ValueError("Takrorlangan warehouse_id aniqlandi.")

    # 6. Numeric turga o'tkazish
    df["warehouse_capacity"] = pd.to_numeric(
        df["warehouse_capacity"],
        errors="raise"
    ).astype("int64")

    # 7. Business Rule tekshiruvi
    if (df["warehouse_capacity"] <= 0).any():
        raise ValueError("Warehouse capacity 0 dan katta bo'lishi kerak.")

    # 8. Silver Layer'ga saqlash
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        SILVER_FILE,
        engine="pyarrow",
        index=False
    )

    print("WAREHOUSES SILVER TRANSFORMATION COMPLETED")
    print(f"Records: {len(df)}")
    print(f"Output: {SILVER_FILE}")


if __name__ == "__main__":
    transform_warehouses()
