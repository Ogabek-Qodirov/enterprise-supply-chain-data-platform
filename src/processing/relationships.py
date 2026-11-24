
import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BRONZE_DIR = PROJECT_ROOT / "data" / "bronze"


def validate_foreign_key(
    child_file: str,
    child_column: str,
    parent_file: str,
    parent_column: str,
    allow_null: bool = False
) -> dict:
    """Check whether child keys exist in the parent table."""

    child_path = BRONZE_DIR / child_file
    parent_path = BRONZE_DIR / parent_file

    if not child_path.exists():
        raise FileNotFoundError(f"Child file not found: {child_path}")

    if not parent_path.exists():
        raise FileNotFoundError(f"Parent file not found: {parent_path}")

    with open(parent_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        if parent_column not in (reader.fieldnames or []):
            raise ValueError(f"Column {parent_column} not found in {parent_file}")

        parent_keys = {
            (row[parent_column] or "").strip()
            for row in reader
            if (row[parent_column] or "").strip()
        }

    total_records = 0
    invalid_references = 0
    missing_values = 0

    with open(child_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        if child_column not in (reader.fieldnames or []):
            raise ValueError(f"Column {child_column} not found in {child_file}")

        for row in reader:
            total_records += 1
            value = (row[child_column] or "").strip()

            if not value:
                if not allow_null:
                    missing_values += 1
                continue

            if value not in parent_keys:
                invalid_references += 1

    passed = invalid_references == 0 and missing_values == 0

    return {
        "child_file": child_file,
        "parent_file": parent_file,
        "total_records": total_records,
        "invalid_references": invalid_references,
        "missing_values": missing_values,
        "passed": passed
    }
