
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

GOLD_FILE = (
    PROJECT_ROOT
    / "data"
    / "gold"
    / "warehouse"
    / "gold_warehouse_performance.parquet"
)


def validate_gold_warehouse_performance():

    print("GOLD WAREHOUSE PERFORMANCE VALIDATION")
    print("=" * 65)

    if not GOLD_FILE.exists():
        raise FileNotFoundError(
            f"Gold dataset not found: {GOLD_FILE}"
        )

    df = pd.read_parquet(GOLD_FILE)

    checks_passed = 0
    checks_failed = 0

    def report_check(name, condition):
        nonlocal checks_passed, checks_failed

        if condition:
            print(f"PASS | {name}")
            checks_passed += 1
        else:
            print(f"FAIL | {name}")
            checks_failed += 1

    # 1. Record count
    report_check(
        "Exactly 5 warehouses",
        len(df) == 5
    )

    # 2. Primary key validation
    report_check(
        "warehouse_id has no NULL values",
        df["warehouse_id"].notna().all()
    )

    report_check(
        "warehouse_id contains no duplicates",
        df["warehouse_id"].is_unique
    )

    # 3. Required columns
    required_columns = [
        "warehouse_id",
        "total_orders",
        "avg_processing_time_minutes",
        "warehouse_operating_cost",
        "total_shipping_cost",
        "completed_handoffs",
        "on_time_handoffs",
        "on_time_handoff_rate",
        "late_handoff_count"
    ]

    columns_exist = all(
        column in df.columns
        for column in required_columns
    )

    report_check(
        "All required columns exist",
        columns_exist
    )

    if not columns_exist:
        print("\nValidation stopped: required columns are missing.")
        return

    # 4. Metrics that allow NULL
    nullable_metrics = [
        "avg_processing_time_minutes",
        "total_shipping_cost"
    ]

    for column in nullable_metrics:

        values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        valid = (
            df[column].isna()
            | (
                values.notna()
                & (values >= 0)
            )
        ).all()

        report_check(
            f"{column} contains non-negative values or NULL",
            valid
        )

    # 5. Metrics that must not contain NULL
    required_numeric_metrics = [
        "total_orders",
        "warehouse_operating_cost",
        "completed_handoffs",
        "on_time_handoffs",
        "late_handoff_count"
    ]

    for column in required_numeric_metrics:

        values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        valid = (
            values.notna()
            & (values >= 0)
        ).all()

        report_check(
            f"{column} contains non-negative values",
            valid
        )

    # 6. Handoff rate validation
    rate = pd.to_numeric(
        df["on_time_handoff_rate"],
        errors="coerce"
    )

    valid_rate = (
        df["on_time_handoff_rate"].isna()
        | (
            rate.notna()
            & rate.between(0, 100)
        )
    ).all()

    report_check(
        "Handoff rate is between 0 and 100 or NULL",
        valid_rate
    )

    # 7. On-time handoffs cannot exceed completed handoffs
    valid_handoffs = (
        df["on_time_handoffs"]
        <= df["completed_handoffs"]
    ).all()

    report_check(
        "On-time handoffs do not exceed completed handoffs",
        valid_handoffs
    )

    # 8. Handoff rate calculation consistency
    completed = df["completed_handoffs"]

    expected_rate = (
        df["on_time_handoffs"]
        / completed.where(completed != 0)
        * 100
    )

    valid_rate_calculation = (
        (
            rate.isna()
            & expected_rate.isna()
        )
        | (
            rate.notna()
            & expected_rate.notna()
            & (rate - expected_rate).abs().le(0.000001)
        )
    ).all()

    report_check(
        "Handoff rate calculation is consistent",
        valid_rate_calculation
    )

    # 9. Final report
    print("\n" + "=" * 65)
    print(f"Total checks passed: {checks_passed}")
    print(f"Total checks failed: {checks_failed}")

    if checks_failed == 0:
        print("\nRESULT: ALL GOLD DATA QUALITY CHECKS PASSED")
    else:
        print("\nRESULT: GOLD DATA QUALITY VALIDATION FAILED")


if __name__ == "__main__":
    validate_gold_warehouse_performance()
