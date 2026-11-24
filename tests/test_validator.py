
from src.processing.validator import validate_csv


TABLES = {
    "oms_customers.csv": "customer_id",
    "oms_products.csv": "product_id",
    "oms_orders.csv": "order_id",
    "oms_order_items.csv": "order_item_id",
    "wms_warehouses.csv": "warehouse_id",
    "wms_employees.csv": "employee_id",
    "wms_inventory.csv": "inventory_id",
    "wms_warehouse_events.csv": "event_id",
    "tms_carriers.csv": "carrier_id",
    "tms_shipments.csv": "shipment_id",
    "tms_delivery_events.csv": "delivery_event_id",
    "finance_order_revenue.csv": "revenue_id",
    "finance_warehouse_expenses.csv": "expense_id",
    "finance_shipping_costs.csv": "shipping_cost_id",
}


def test_all_tables():
    total_records = 0
    failed_tables = []

    print("\nDATA QUALITY REPORT")
    print("=" * 75)

    for filename, primary_key in TABLES.items():
        result = validate_csv(filename, primary_key)

        total_records += result["total_records"]

        status = "PASS" if result["passed"] else "FAIL"

        print(
            f"{status} | {filename:<35} "
            f"Records: {result['total_records']:<5} "
            f"Missing: {result['missing_primary_keys']:<3} "
            f"Duplicates: {result['duplicate_primary_keys']}"
        )

        if not result["passed"]:
            failed_tables.append(filename)

    print("=" * 75)
    print(f"Tables checked: {len(TABLES)}")
    print(f"Total records: {total_records}")
    print(f"Failed tables: {len(failed_tables)}")

    if failed_tables:
        print("Failed:", failed_tables)
        raise AssertionError("Data quality validation failed.")

    print("RESULT: ALL TABLES PASSED")


if __name__ == "__main__":
    test_all_tables()
