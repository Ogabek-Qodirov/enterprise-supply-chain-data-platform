
import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def validate_csv(
    filename: str,
    primary_key: str
) -> dict:
    """Validate CSV data without loading the entire file into memory."""

    file_path = PROJECT_ROOT / "data" / "bronze" / filename

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    total_records = 0
    missing_keys = 0
    primary_key_values = set()
    duplicate_keys = 0

    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        if primary_key not in (reader.fieldnames or []):
            raise ValueError(
                f"Primary key '{primary_key}' not found in {filename}"
            )

        for row in reader:
            total_records += 1

            key = (row.get(primary_key) or "").strip()

            if not key:
                missing_keys += 1
                continue

            if key in primary_key_values:
                duplicate_keys += 1
            else:
                primary_key_values.add(key)

    result = {
        "filename": filename,
        "total_records": total_records,
        "missing_primary_keys": missing_keys,
        "duplicate_primary_keys": duplicate_keys,
        "passed": missing_keys == 0 and duplicate_keys == 0
    }

    return result
