
from src.ingestion.extractor import extract_to_csv


def extract_warehouse_expenses():
    """Extract warehouse expenses from the Finance source system."""

    query = """
        SELECT
            expense_id,
            warehouse_id,
            expense_category,
            expense_amount,
            expense_timestamp,
            description
        FROM finance.warehouse_expenses
    """

    extract_to_csv(
        query=query,
        output_filename="finance_warehouse_expenses.csv"
    )


if __name__ == "__main__":
    extract_warehouse_expenses()
