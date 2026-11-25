
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
SILVER_DIR = BASE_DIR / "data" / "silver"


TABLES = {
    "oms/customers": {
        "count": 5,
        "pk": "customer_id",
    },
    "oms/products": {
        "count": 6,
        "pk": "product_id",
    },
    "oms/orders": {
        "count": 5,
        "pk": "order_id",
    },
    "oms/order_items": {
        "count": 8,
        "pk": "order_item_id",
    },
    "wms/warehouses": {
        "count": 5,
        "pk": "warehouse_id",
    },
    "wms/employees": {
        "count": 10,
        "pk": "employee_id",
    },
    "wms/inventory": {
        "count": 15,
        "pk": "inventory_id",
    },
    "wms/warehouse_events": {
        "count": 22,
        "pk": "event_id",
    },
    "tms/carriers": {
        "count": 3,
        "pk": "carrier_id",
    },
    "tms/shipments": {
        "count": 5,
        "pk": "shipment_id",
    },
    "tms/delivery_events": {
        "count": 14,
        "pk": "delivery_event_id",
    },
    "finance/order_revenue": {
        "count": 5,
        "pk": "revenue_id",
    },
    "finance/warehouse_expenses": {
        "count": 15,
        "pk": "expense_id",
    },
    "finance/shipping_costs": {
        "count": 6,
        "pk": "shipping_cost_id",
    },
}


RELATIONSHIPS = [
    ("oms/orders", "customer_id", "oms/customers", "customer_id"),
    ("oms/order_items", "order_id", "oms/orders", "order_id"),
    ("oms/order_items", "product_id", "oms/products", "product_id"),
    ("wms/employees", "warehouse_id", "wms/warehouses", "warehouse_id"),
    ("wms/inventory", "warehouse_id", "wms/warehouses", "warehouse_id"),
    ("wms/inventory", "product_id", "oms/products", "product_id"),
    ("wms/warehouse_events", "order_id", "oms/orders", "order_id"),
    ("wms/warehouse_events", "warehouse_id", "wms/warehouses", "warehouse_id"),
    ("wms/warehouse_events", "employee_id", "wms/employees", "employee_id"),
    ("tms/shipments", "order_id", "oms/orders", "order_id"),
    ("tms/shipments", "carrier_id", "tms/carriers", "carrier_id"),
    ("tms/shipments", "warehouse_id", "wms/warehouses", "warehouse_id"),
    ("tms/delivery_events", "shipment_id", "tms/shipments", "shipment_id"),
    ("finance/order_revenue", "order_id", "oms/orders", "order_id"),
    ("finance/warehouse_expenses", "warehouse_id", "wms/warehouses", "warehouse_id"),
    ("finance/shipping_costs", "shipment_id", "tms/shipments", "shipment_id"),
]


def load_silver_table(table_name):
    file_path = SILVER_DIR / f"{table_name}.parquet"

    if not file_path.exists():
        return None

    return pd.read_parquet(file_path)


def validate_silver():
    print("=" * 70)
    print("SILVER LAYER VALIDATION REPORT")
    print("=" * 70)

    failed_checks = 0
    total_records = 0
    loaded_tables = {}

    # 1. Fayllar, record count va Primary Key tekshiruvi
    print("\n1. TABLE AND PRIMARY KEY VALIDATION")

    for table_name, config in TABLES.items():
        df = load_silver_table(table_name)

        if df is None:
            print(f"FAIL | {table_name} | File not found")
            failed_checks += 1
            continue

        loaded_tables[table_name] = df
        total_records += len(df)

        count_ok = len(df) == config["count"]
        pk = config["pk"]

        pk_ok = (
            pk in df.columns
            and not df[pk].isna().any()
            and not df[pk].duplicated().any()
        )

        if count_ok and pk_ok:
            print(
                f"PASS | {table_name} | "
                f"Records: {len(df)} | PK: {pk}"
            )
        else:
            print(
                f"FAIL | {table_name} | "
                f"Records: {len(df)} | "
                f"Expected: {config['count']} | PK valid: {pk_ok}"
            )
            failed_checks += 1

    # 2. Foreign Key tekshiruvi
    print("\n2. FOREIGN KEY VALIDATION")

    for child, child_key, parent, parent_key in RELATIONSHIPS:
        child_df = loaded_tables.get(child)
        parent_df = loaded_tables.get(parent)

        if child_df is None or parent_df is None:
            print(f"FAIL | {child}.{child_key} -> {parent}.{parent_key}")
            failed_checks += 1
            continue

        if child_key not in child_df.columns or parent_key not in parent_df.columns:
            print(f"FAIL | Missing relationship column: {child_key}")
            failed_checks += 1
            continue

        valid_keys = set(parent_df[parent_key].dropna())

        # NULL qiymatlar, masalan, warehouse_events.employee_id,
        # ruxsat etilgan holat sifatida qoldiriladi.
        child_keys = child_df[child_key].dropna()

        invalid_keys = child_keys[~child_keys.isin(valid_keys)]

        if invalid_keys.empty:
            print(f"PASS | {child}.{child_key} -> {parent}.{parent_key}")
        else:
            print(
                f"FAIL | {child}.{child_key} -> {parent}.{parent_key} | "
                f"Invalid values: {invalid_keys.tolist()}"
            )
            failed_checks += 1

    # 3. Yakuniy hisobot
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    print(f"Tables checked: {len(loaded_tables)}/{len(TABLES)}")
    print(f"Relationships checked: {len(RELATIONSHIPS)}")
    print(f"Total records: {total_records}")
    print(f"Failed checks: {failed_checks}")

    if failed_checks == 0 and len(loaded_tables) == len(TABLES):
        print("\nRESULT: ALL SILVER LAYER CHECKS PASSED")
    else:
        print("\nRESULT: SILVER LAYER VALIDATION FAILED")

        raise ValueError("Silver Layer validation failed.")


if __name__ == "__main__":
    validate_silver()
