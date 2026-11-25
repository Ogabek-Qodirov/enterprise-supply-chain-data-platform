
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BRONZE_FILE = PROJECT_ROOT / "data" / "bronze" / "oms_orders.csv"
SILVER_CUSTOMERS = PROJECT_ROOT / "data" / "silver" / "oms" / "customers.parquet"

SILVER_DIR = PROJECT_ROOT / "data" / "silver" / "oms"
SILVER_FILE = SILVER_DIR / "orders.parquet"


def transform_orders():
    # 1. Read Bronze data
    df = pd.read_csv(BRONZE_FILE)

    # 2. Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # 3. Clean text columns
    for column in ["order_id", "customer_id", "order_status"]:
        df[column] = df[column].astype("string").str.strip()

    # 4. Validate required values
    required_columns = [
        "order_id",
        "customer_id",
        "order_status",
        "order_timestamp"
    ]

    if df[required_columns].isna().any().any():
        raise ValueError("Missing required order values detected.")

    if (df["order_id"] == "").any():
        raise ValueError("Empty order IDs detected.")

    # 5. Validate primary key
    if df["order_id"].duplicated().any():
        raise ValueError("Duplicate order IDs detected.")

    # 6. Convert timestamp
    df["order_timestamp"] = pd.to_datetime(
        df["order_timestamp"],
        errors="raise"
    )

    # 7. Validate customer relationships
    customers = pd.read_parquet(SILVER_CUSTOMERS)

    valid_customer_ids = set(
        customers["customer_id"].astype("string")
    )

    invalid_customers = ~df["customer_id"].isin(valid_customer_ids)

    if invalid_customers.any():
        raise ValueError(
            f"Orders contain {invalid_customers.sum()} "
            "invalid customer references."
        )

    # 8. Save Silver data
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        SILVER_FILE,
        engine="pyarrow",
        index=False
    )

    print("ORDERS SILVER TRANSFORMATION COMPLETED")
    print(f"Records: {len(df)}")
    print(f"Output: {SILVER_FILE}")


if __name__ == "__main__":
    transform_orders()
