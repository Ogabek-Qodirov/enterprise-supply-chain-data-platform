from src.ingestion.extractor import extract_to_csv


def extract_inventory():
    """Extract inventory from the WMS source system."""

    query = """
        SELECT
            inventory_id,
            warehouse_id,
            product_id,
            quantity,
            last_updated_at
        FROM wms.inventory
    """

    extract_to_csv(
        query=query,
        output_filename="wms_inventory.csv"
    )


if __name__ == "__main__":
    extract_inventory()