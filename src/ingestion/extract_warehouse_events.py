from src.ingestion.extractor import extract_to_csv


def extract_warehouse_events():
    """Extract warehouse events from the WMS source system."""

    query = """
        SELECT
            event_id,
            order_id,
            warehouse_id,
            employee_id,
            event_type,
            event_timestamp,
            ingested_at
        FROM wms.warehouse_events
    """

    extract_to_csv(
        query=query,
        output_filename="wms_warehouse_events.csv"
    )


if __name__ == "__main__":
    extract_warehouse_events()