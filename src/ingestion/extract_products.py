from src.ingestion.extractor import extract_to_csv


def extract_products():
    """Extract products from the OMS source system."""

    query = """
        SELECT
            product_id,
            product_name,
            category,
            unit_price
        FROM oms.products
    """

    extract_to_csv(
        query=query,
        output_filename="oms_products.csv"
    )


if __name__ == "__main__":
    extract_products()