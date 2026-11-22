
from src.ingestion.extractor import extract_to_csv


def extract_shipping_costs():
    """Extract shipping costs from the Finance source system."""

    query = """
        SELECT
            shipping_cost_id,
            shipment_id,
            shipping_amount,
            recorded_at,
            description
        FROM finance.shipping_costs
    """

    extract_to_csv(
        query=query,
        output_filename="finance_shipping_costs.csv"
    )


if __name__ == "__main__":
    extract_shipping_costs()
