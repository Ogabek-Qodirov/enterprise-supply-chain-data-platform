from src.ingestion.extractor import extract_to_csv


def extract_delivery_events():
    """Extract delivery events from the TMS source system."""

    query = """
        SELECT
            delivery_event_id,
            shipment_id,
            event_type,
            event_timestamp,
            ingested_at,
            event_location
        FROM tms.delivery_events
    """

    extract_to_csv(
        query=query,
        output_filename="tms_delivery_events.csv"
    )


if __name__ == "__main__":
    extract_delivery_events()