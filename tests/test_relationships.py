
from src.processing.relationships import validate_foreign_key


RELATIONSHIPS = [
    {
        "child_file": "oms_orders.csv",
        "child_column": "customer_id",
        "parent_file": "oms_customers.csv",
        "parent_column": "customer_id",
    },
    {
        "child_file": "oms_order_items.csv",
        "child_column": "order_id",
        "parent_file": "oms_orders.csv",
        "parent_column": "order_id",
    },
    {
        "child_file": "oms_order_items.csv",
        "child_column": "product_id",
        "parent_file": "oms_products.csv",
        "parent_column": "product_id",
    },
]


def test_oms_relationships():
    print("\nOMS FOREIGN KEY VALIDATION")
    print("=" * 65)

    failed_relationships = []

    for relationship in RELATIONSHIPS:
        result = validate_foreign_key(**relationship)

        status = "PASS" if result["passed"] else "FAIL"

        print(
            f"{status} | "
            f"{result['child_file']}.{relationship['child_column']} "
            f"-> {result['parent_file']}.{relationship['parent_column']} "
            f"| Invalid: {result['invalid_references']} "
            f"| Missing: {result['missing_values']}"
        )

        if not result["passed"]:
            failed_relationships.append(relationship)

    print("=" * 65)
    print(f"Relationships checked: {len(RELATIONSHIPS)}")
    print(f"Failed relationships: {len(failed_relationships)}")

    assert not failed_relationships, "OMS relationship validation failed."


RELATIONSHIPS = [
    # OMS
    {
        "child_file": "oms_orders.csv",
        "child_column": "customer_id",
        "parent_file": "oms_customers.csv",
        "parent_column": "customer_id",
    },
    {
        "child_file": "oms_order_items.csv",
        "child_column": "order_id",
        "parent_file": "oms_orders.csv",
        "parent_column": "order_id",
    },
    {
        "child_file": "oms_order_items.csv",
        "child_column": "product_id",
        "parent_file": "oms_products.csv",
        "parent_column": "product_id",
    },

    # WMS
    {
        "child_file": "wms_employees.csv",
        "child_column": "warehouse_id",
        "parent_file": "wms_warehouses.csv",
        "parent_column": "warehouse_id",
    },
    {
        "child_file": "wms_inventory.csv",
        "child_column": "warehouse_id",
        "parent_file": "wms_warehouses.csv",
        "parent_column": "warehouse_id",
    },
    {
        "child_file": "wms_inventory.csv",
        "child_column": "product_id",
        "parent_file": "oms_products.csv",
        "parent_column": "product_id",
    },
    {
        "child_file": "wms_warehouse_events.csv",
        "child_column": "order_id",
        "parent_file": "oms_orders.csv",
        "parent_column": "order_id",
    },
    {
        "child_file": "wms_warehouse_events.csv",
        "child_column": "warehouse_id",
        "parent_file": "wms_warehouses.csv",
        "parent_column": "warehouse_id",
    },
    {
        "child_file": "wms_warehouse_events.csv",
        "child_column": "employee_id",
        "parent_file": "wms_employees.csv",
        "parent_column": "employee_id",
        "allow_null": True,
    },

    # TMS
    {
        "child_file": "tms_shipments.csv",
        "child_column": "order_id",
        "parent_file": "oms_orders.csv",
        "parent_column": "order_id",
    },
    {
        "child_file": "tms_shipments.csv",
        "child_column": "carrier_id",
        "parent_file": "tms_carriers.csv",
        "parent_column": "carrier_id",
    },
    {
        "child_file": "tms_shipments.csv",
        "child_column": "warehouse_id",
        "parent_file": "wms_warehouses.csv",
        "parent_column": "warehouse_id",
    },
    {
        "child_file": "tms_delivery_events.csv",
        "child_column": "shipment_id",
        "parent_file": "tms_shipments.csv",
        "parent_column": "shipment_id",
    },

    # Finance
    {
        "child_file": "finance_order_revenue.csv",
        "child_column": "order_id",
        "parent_file": "oms_orders.csv",
        "parent_column": "order_id",
    },
    {
        "child_file": "finance_warehouse_expenses.csv",
        "child_column": "warehouse_id",
        "parent_file": "wms_warehouses.csv",
        "parent_column": "warehouse_id",
    },
    {
        "child_file": "finance_shipping_costs.csv",
        "child_column": "shipment_id",
        "parent_file": "tms_shipments.csv",
        "parent_column": "shipment_id",
    },
]


if __name__ == "__main__":
    test_oms_relationships()
