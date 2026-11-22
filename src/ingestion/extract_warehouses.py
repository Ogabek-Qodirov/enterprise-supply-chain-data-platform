from src.ingestion.extractor import extract_to_csv


def extract_warehouses():
    """Extract warehouses from the WMS source system."""

    query = """
        SELECT
            warehouse_id,
            warehouse_name,
            city,
            warehouse_capacity,
            created_at
        FROM wms.warehouses
    """

    extract_to_csv(
        query=query,
        output_filename="wms_warehouses.csv"
    )


if __name__ == "__main__":
    extract_warehouses()