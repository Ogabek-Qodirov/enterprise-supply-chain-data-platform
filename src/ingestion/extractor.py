
import csv
from pathlib import Path

from src.ingestion.database import get_connection


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BRONZE_DIR = PROJECT_ROOT / "data" / "bronze"


def extract_to_csv(query: str, output_filename: str) -> int:
    """
    Execute a SQL query and save the results as a CSV file.

    Returns the number of extracted records.
    """

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(query)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        BRONZE_DIR.mkdir(parents=True, exist_ok=True)

        output_file = BRONZE_DIR / output_filename

        with open(output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow(columns)
            writer.writerows(rows)

        print(f"Extracted {len(rows)} records.")
        print(f"Saved to: {output_file}")

        return len(rows)

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()
