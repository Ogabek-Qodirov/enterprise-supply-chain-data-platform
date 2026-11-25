
import pandas as pd
from decimal import Decimal
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BRONZE_FILE = PROJECT_ROOT / "data" / "bronze" / "oms_products.csv"
SILVER_DIR = PROJECT_ROOT / "data" / "silver" / "oms"
SILVER_FILE = SILVER_DIR / "products.parquet"


def transform_products():
    # 1. Read Bronze data
    df = pd.read_csv(BRONZE_FILE)

    # 2. Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # 3. Clean text columns
    for column in ["product_id", "product_name", "category"]:
        df[column] = df[column].astype("string").str.strip()

    # 4. Validate required fields
    required_columns = ["product_id", "product_name", "category", "unit_price"]

    if df[required_columns].isna().any().any():
        raise ValueError("Missing required product values detected.")

    if (df["product_id"] == "").any():
        raise ValueError("Empty product IDs detected.")

    # 5. Validate primary key
    if df["product_id"].duplicated().any():
        raise ValueError("Duplicate product IDs detected.")

    # 6. Convert prices to Decimal
    df["unit_price"] = df["unit_price"].map(
        lambda value: Decimal(str(value))
    )

    if (df["unit_price"] < Decimal("0")).any():
        raise ValueError("Negative product prices detected.")

    # 7. Save Silver data
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        SILVER_FILE,
        engine="pyarrow",
        index=False
    )

    print("PRODUCTS SILVER TRANSFORMATION COMPLETED")
    print(f"Records: {len(df)}")
    print(f"Output: {SILVER_FILE}")


if __name__ == "__main__":
    transform_products()
