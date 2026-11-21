from src.ingestion.extractor import extract_to_csv


def extract_order_items():
    """Extract order items from the OMS source system."""

    query = """
        SELECT
            order_item_id,
            order_id,
            product_id,
            quantity,
            unit_price
        FROM oms.order_items
    """

    extract_to_csv(
        query=query,
        output_filename="oms_order_items.csv"
    )


if __name__ == "__main__":
    extract_order_items()