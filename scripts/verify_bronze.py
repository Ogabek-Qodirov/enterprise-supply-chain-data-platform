
import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BRONZE_DIR = PROJECT_ROOT / "data" / "bronze"

EXPECTED_COUNTS = {
    "oms_customers.csv": 5,
    "oms_products.csv": 6,
    "oms_orders.csv": 5,
    "oms_order_items.csv": 8,
    "wms_warehouses.csv": 5,
    "wms_employees.csv": 10,
    "wms_inventory.csv": 15,
    "wms_warehouse_events.csv": 22,
    "tms_carriers.csv": 3,
    "tms_shipments.csv": 5,
    "tms_delivery_events.csv": 14,
    "finance_order_revenue.csv": 5,
    "finance_warehouse_expenses.csv": 15,
    "finance_shipping_costs.csv": 6,
}


def verify_bronze():
    total_records = 0
    all_passed = True

    print("BRONZE LAYER VERIFICATION")
    print("-" * 55)

    for filename, expected_count in EXPECTED_COUNTS.items():
        file_path = BRONZE_DIR / filename

        if not file_path.exists():
            print(f"MISSING: {filename}")
            all_passed = False
            continue

        with open(file_path, "r", encoding="utf-8", newline="") as file:
            actual_count = sum(1 for _ in csv.DictReader(file))

        total_records += actual_count

        if actual_count == expected_count:
            print(f"PASS: {filename} - {actual_count} records")
        else:
            print(
                f"FAIL: {filename} - "
                f"Expected {expected_count}, got {actual_count}"
            )
            all_passed = False

    print("-" * 55)
    print(f"Total records: {total_records}")
    print(f"Expected records: {sum(EXPECTED_COUNTS.values())}")

    if all_passed and total_records == sum(EXPECTED_COUNTS.values()):
        print("RESULT: ALL CHECKS PASSED")
    else:
        print("RESULT: VERIFICATION FAILED")


if __name__ == "__main__":
    verify_bronze()
