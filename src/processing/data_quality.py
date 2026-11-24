
from src.processing.validator import validate_csv
from src.processing.relationships import validate_foreign_key


TABLES = {
    "oms_customers.csv": ("customer_id", 5),
    "oms_products.csv": ("product_id", 6),
    "oms_orders.csv": ("order_id", 5),
    "oms_order_items.csv": ("order_item_id", 8),
    "wms_warehouses.csv": ("warehouse_id", 5),
    "wms_employees.csv": ("employee_id", 10),
    "wms_inventory.csv": ("inventory_id", 15),
    "wms_warehouse_events.csv": ("event_id", 22),
    "tms_carriers.csv": ("carrier_id", 3),
    "tms_shipments.csv": ("shipment_id", 5),
    "tms_delivery_events.csv": ("delivery_event_id", 14),
    "finance_order_revenue.csv": ("revenue_id", 5),
    "finance_warehouse_expenses.csv": ("expense_id", 15),
    "finance_shipping_costs.csv": ("shipping_cost_id", 6),
}


RELATIONSHIPS = [
    ("oms_orders.csv", "customer_id", "oms_customers.csv", "customer_id", False),
    ("oms_order_items.csv", "order_id", "oms_orders.csv", "order_id", False),
    ("oms_order_items.csv", "product_id", "oms_products.csv", "product_id", False),
    ("wms_employees.csv", "warehouse_id", "wms_warehouses.csv", "warehouse_id", False),
    ("wms_inventory.csv", "warehouse_id", "wms_warehouses.csv", "warehouse_id", False),
    ("wms_inventory.csv", "product_id", "oms_products.csv", "product_id", False),
    ("wms_warehouse_events.csv", "order_id", "oms_orders.csv", "order_id", False),
    ("wms_warehouse_events.csv", "warehouse_id", "wms_warehouses.csv", "warehouse_id", False),
    ("wms_warehouse_events.csv", "employee_id", "wms_employees.csv", "employee_id", True),
    ("tms_shipments.csv", "order_id", "oms_orders.csv", "order_id", False),
    ("tms_shipments.csv", "carrier_id", "tms_carriers.csv", "carrier_id", False),
    ("tms_shipments.csv", "warehouse_id", "wms_warehouses.csv", "warehouse_id", False),
    ("tms_delivery_events.csv", "shipment_id", "tms_shipments.csv", "shipment_id", False),
    ("finance_order_revenue.csv", "order_id", "oms_orders.csv", "order_id", False),
    ("finance_warehouse_expenses.csv", "warehouse_id", "wms_warehouses.csv", "warehouse_id", False),
    ("finance_shipping_costs.csv", "shipment_id", "tms_shipments.csv", "shipment_id", False),
]


def run_data_quality():
    failed_checks = 0
    total_records = 0

    print("\nENTERPRISE DATA QUALITY REPORT")
    print("=" * 75)

    print("\n1. PRIMARY KEY VALIDATION")

    for filename, (primary_key, expected_count) in TABLES.items():
        result = validate_csv(filename, primary_key)
        total_records += result["total_records"]

        count_passed = result["total_records"] == expected_count
        passed = result["passed"] and count_passed

        if not passed:
            failed_checks += 1

        status = "PASS" if passed else "FAIL"

        print(
            f"{status} | {filename} | "
            f"Records: {result['total_records']} | "
            f"Missing keys: {result['missing_primary_keys']} | "
            f"Duplicate keys: {result['duplicate_primary_keys']}"
        )

        if not count_passed:
            print(f"  Expected records: {expected_count}")

    print("\n2. FOREIGN KEY VALIDATION")

    for child, child_col, parent, parent_col, allow_null in RELATIONSHIPS:
        result = validate_foreign_key(
            child_file=child,
            child_column=child_col,
            parent_file=parent,
            parent_column=parent_col,
            allow_null=allow_null
        )

        if not result["passed"]:
            failed_checks += 1

        status = "PASS" if result["passed"] else "FAIL"

        print(
            f"{status} | {child}.{child_col} -> "
            f"{parent}.{parent_col} | "
            f"Invalid: {result['invalid_references']} | "
            f"Missing: {result['missing_values']}"
        )

    print("\n" + "=" * 75)
    print(f"Tables checked: {len(TABLES)}")
    print(f"Relationships checked: {len(RELATIONSHIPS)}")
    print(f"Total records: {total_records}")
    print(f"Failed checks: {failed_checks}")

    if failed_checks:
        print("RESULT: DATA QUALITY CHECKS FAILED")
        return False

    print("RESULT: ALL DATA QUALITY CHECKS PASSED")
    return True


if __name__ == "__main__":
    run_data_quality()
