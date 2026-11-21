from src.ingestion.extractor import extract_to_csv


def extract_orders():
    """Extract orders from the OMS source system."""

    query = """
        SELECT
            order_id,
            customer_id,
            order_status,
            order_timestamp
        FROM oms.orders
    """

    extract_to_csv(
        query=query,
        output_filename="oms_orders.csv"
    )


if __name__ == "__main__":
    extract_orders()