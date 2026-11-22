from src.ingestion.extractor import extract_to_csv


def extract_shipments():
    """Extract shipments from the TMS source system."""

    query = """
        SELECT
            shipment_id,
            order_id,
            carrier_id,
            warehouse_id,
            required_handoff_at,
            actual_handoff_at,
            expected_delivery_at,
            actual_delivery_at,
            shipment_status
        FROM tms.shipments
    """

    extract_to_csv(
        query=query,
        output_filename="tms_shipments.csv"
    )


if __name__ == "__main__":
    extract_shipments()