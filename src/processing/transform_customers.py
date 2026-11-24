
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BRONZE_FILE = PROJECT_ROOT / "data" / "bronze" / "oms_customers.csv"
SILVER_DIR = PROJECT_ROOT / "data" / "silver" / "oms"
SILVER_FILE = SILVER_DIR / "customers.parquet"


def transform_customers():
    # 1. Read Bronze data
    df = pd.read_csv(BRONZE_FILE)

    print("BRONZE DATA")
    print(df.info())

    # 2. Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # 3. Clean text columns
    df["customer_id"] = df["customer_id"].astype("string").str.strip()
    df["full_name"] = df["full_name"].astype("string").str.strip()
    df["email"] = df["email"].astype("string").str.strip().str.lower()

    # 4. Convert timestamp
    df["created_at"] = pd.to_datetime(df["created_at"], errors="raise")

    # 5. Validate primary key
    if df["customer_id"].isna().any():
        raise ValueError("Missing customer IDs detected.")

    if df["customer_id"].duplicated().any():
        raise ValueError("Duplicate customer IDs detected.")

    # 6. Save Silver data as Parquet
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        SILVER_FILE,
        engine="pyarrow",
        index=False
    )

    print("\nSILVER TRANSFORMATION COMPLETED")
    print(f"Records: {len(df)}")
    print(f"Output: {SILVER_FILE}")


if __name__ == "__main__":
    transform_customers()
