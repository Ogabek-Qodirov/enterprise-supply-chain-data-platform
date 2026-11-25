
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BRONZE_FILE = (
    PROJECT_ROOT / "data" / "bronze" / "wms_warehouse_events.csv"
)

SILVER_ORDERS = (
    PROJECT_ROOT / "data" / "silver" / "oms" / "orders.parquet"
)

SILVER_WAREHOUSES = (
    PROJECT_ROOT / "data" / "silver" / "wms" / "warehouses.parquet"
)

SILVER_EMPLOYEES = (
    PROJECT_ROOT / "data" / "silver" / "wms" / "employees.parquet"
)

SILVER_DIR = PROJECT_ROOT / "data" / "silver" / "wms"
SILVER_FILE = SILVER_DIR / "warehouse_events.parquet"


def transform_warehouse_events():

    # 1. Bronze ma'lumotlarini o'qish
    df = pd.read_csv(BRONZE_FILE)

    # 2. Ustun nomlarini standartlashtirish
    df.columns = df.columns.str.strip().str.lower()

    # 3. Matn ustunlarini tozalash
    text_columns = [
        "order_id",
        "warehouse_id",
        "employee_id",
        "event_type"
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # 4. Majburiy qiymatlarni tekshirish
    required_columns = [
        "event_id",
        "order_id",
        "warehouse_id",
        "event_type",
        "event_timestamp",
        "ingested_at"
    ]

    if df[required_columns].isna().any().any():
        raise ValueError("Majburiy event qiymatlarida NULL aniqlandi.")

    # 5. Primary Key tekshiruvi
    if df["event_id"].duplicated().any():
        raise ValueError("Takrorlangan event_id aniqlandi.")

    # 6. Numeric formatga o'tkazish
    df["event_id"] = pd.to_numeric(
        df["event_id"],
        errors="raise"
    ).astype("int64")

    # 7. Timestamp formatiga o'tkazish
    for column in ["event_timestamp", "ingested_at"]:
        df[column] = pd.to_datetime(
            df[column],
            errors="raise"
        )

    # 8. Foreign Key tekshiruvlari
    orders = pd.read_parquet(SILVER_ORDERS)
    warehouses = pd.read_parquet(SILVER_WAREHOUSES)
    employees = pd.read_parquet(SILVER_EMPLOYEES)

    valid_order_ids = set(orders["order_id"])
    valid_warehouse_ids = set(warehouses["warehouse_id"])
    valid_employee_ids = set(employees["employee_id"])

    if not df["order_id"].isin(valid_order_ids).all():
        raise ValueError("Noto'g'ri order_id aniqlandi.")

    if not df["warehouse_id"].isin(valid_warehouse_ids).all():
        raise ValueError("Noto'g'ri warehouse_id aniqlandi.")

    # employee_id NULL bo'lishi mumkin.
    assigned_employees = df["employee_id"].dropna()

    if not assigned_employees.isin(valid_employee_ids).all():
        raise ValueError("Noto'g'ri employee_id aniqlandi.")

    # 9. Event vaqtlarini tekshirish
    if (df["ingested_at"] < df["event_timestamp"]).any():
        raise ValueError(
            "Ingestion vaqti event sodir bo'lgan vaqtdan oldin."
        )

    # 10. Silver Layer'ga saqlash
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        SILVER_FILE,
        engine="pyarrow",
        index=False
    )

    print("WAREHOUSE EVENTS SILVER TRANSFORMATION COMPLETED")
    print(f"Records: {len(df)}")
    print(f"Output: {SILVER_FILE}")


if __name__ == "__main__":
    transform_warehouse_events()
