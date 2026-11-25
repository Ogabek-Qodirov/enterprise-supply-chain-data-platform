
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BRONZE_FILE = (
    PROJECT_ROOT / "data" / "bronze" / "wms_employees.csv"
)

SILVER_WAREHOUSES = (
    PROJECT_ROOT / "data" / "silver" / "wms" / "warehouses.parquet"
)

SILVER_DIR = PROJECT_ROOT / "data" / "silver" / "wms"
SILVER_FILE = SILVER_DIR / "employees.parquet"


def transform_employees():

    # 1. Bronze ma'lumotlarini o'qish
    df = pd.read_csv(BRONZE_FILE)

    # 2. Ustun nomlarini standartlashtirish
    df.columns = df.columns.str.strip().str.lower()

    # 3. Matn ustunlarini tozalash
    text_columns = [
        "employee_id",
        "warehouse_id",
        "full_name",
        "job_title"
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # 4. Majburiy qiymatlarni tekshirish
    required_columns = [
        "employee_id",
        "warehouse_id",
        "full_name",
        "job_title",
        "hire_date"
    ]

    if df[required_columns].isna().any().any():
        raise ValueError("Majburiy qiymatlarda NULL aniqlandi.")

    # 5. Primary Key tekshiruvi
    if df["employee_id"].duplicated().any():
        raise ValueError("Takrorlangan employee_id aniqlandi.")

    # 6. Sanani datetime formatiga o'tkazish
    df["hire_date"] = pd.to_datetime(
        df["hire_date"],
        errors="raise"
    )

    # 7. Foreign Key tekshiruvi
    warehouses = pd.read_parquet(SILVER_WAREHOUSES)

    valid_warehouse_ids = set(warehouses["warehouse_id"])

    invalid_warehouses = ~df["warehouse_id"].isin(
        valid_warehouse_ids
    )

    if invalid_warehouses.any():
        raise ValueError(
            f"{invalid_warehouses.sum()} ta noto'g'ri warehouse_id aniqlandi."
        )

    # 8. Silver Layer'ga saqlash
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        SILVER_FILE,
        engine="pyarrow",
        index=False
    )

    print("EMPLOYEES SILVER TRANSFORMATION COMPLETED")
    print(f"Records: {len(df)}")
    print(f"Output: {SILVER_FILE}")


if __name__ == "__main__":
    transform_employees()
