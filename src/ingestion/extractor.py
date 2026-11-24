
import csv
from datetime import datetime
from pathlib import Path

from src.ingestion.database import get_connection
from src.ingestion.logger import get_logger
from src.ingestion.audit import record_audit


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BRONZE_DIR = PROJECT_ROOT / "data" / "bronze"

BATCH_SIZE = 1000

logger = get_logger("ingestion")


def extract_to_csv(query: str, output_filename: str) -> int:
    """
    Extract SQL query results in batches and save them to CSV.
    Record execution details in the ingestion audit file.

    Returns the total number of extracted records.
    """

    connection = None
    cursor = None
    total_records = 0
    start_time = datetime.now()
    status = "FAILED"
    error_message = ""

    try:
        logger.info("Starting extraction: %s", output_filename)

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)

        columns = [column[0] for column in cursor.description]

        BRONZE_DIR.mkdir(parents=True, exist_ok=True)
        output_file = BRONZE_DIR / output_filename

        with open(output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(columns)

            while True:
                rows = cursor.fetchmany(BATCH_SIZE)

                if not rows:
                    break

                writer.writerows(rows)
                total_records += len(rows)

        status = "SUCCESS"

        logger.info(
            "Extraction completed: %s | Records: %s",
            output_filename,
            total_records
        )

        logger.info("Output file: %s", output_file)

        return total_records

    except Exception as error:
        error_message = str(error)

        logger.exception("Extraction failed: %s", output_filename)
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

        end_time = datetime.now()

        record_audit(
            table_name=output_filename,
            start_time=start_time,
            end_time=end_time,
            records_extracted=total_records,
            status=status,
            error_message=error_message
        )
