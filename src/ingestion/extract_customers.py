
from src.ingestion.extractor import extract_to_csv


def extract_customers():
    """Extract customers from the OMS source system."""

    query = """
        SELECT
            customer_id,
            full_name,
            email,
            created_at
        FROM oms.customers
    """

    extract_to_csv(
        query=query,
        output_filename="oms_customers.csv"
    )


if __name__ == "__main__":
    extract_customers()
