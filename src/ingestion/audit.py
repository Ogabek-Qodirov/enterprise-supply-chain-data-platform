
import csv
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUDIT_DIR = PROJECT_ROOT / "data" / "audit"

AUDIT_FILE = AUDIT_DIR / "ingestion_audit.csv"


def record_audit(
    table_name: str,
    start_time: datetime,
    end_time: datetime,
    records_extracted: int,
    status: str,
    error_message: str = ""
):
    """Record the result of a single table extraction."""

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    file_exists = AUDIT_FILE.exists()

    with open(AUDIT_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "table_name",
                "start_time",
                "end_time",
                "duration_seconds",
                "records_extracted",
                "status",
                "error_message"
            ])

        duration = (end_time - start_time).total_seconds()

        writer.writerow([
            table_name,
            start_time.isoformat(),
            end_time.isoformat(),
            duration,
            records_extracted,
            status,
            error_message
        ])
