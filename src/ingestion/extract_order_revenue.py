from src.ingestion.extractor import extract_to_csv


def extract_order_revenue():
    """Extract order revenue from the Finance source system."""

    query = """
        SELECT
            revenue_id,
            order_id,
            revenue_amount,
            recognized_at
        FROM finance.order_revenue
    """

    extract_to_csv(
        query=query,
        output_filename="finance_order_revenue.csv"
    )


if __name__ == "__main__":
    extract_order_revenue()