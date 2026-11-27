
from pathlib import Path

import pandas as pd


# Project directories
PROJECT_ROOT = Path(__file__).resolve().parents[3]

SILVER_DIR = PROJECT_ROOT / "data" / "silver"
GOLD_DIR = PROJECT_ROOT / "data" / "gold" / "warehouse"


def load_silver_data():
    """Load required Silver datasets."""

    warehouses = pd.read_parquet(
        SILVER_DIR / "wms" / "warehouses.parquet"
    )

    shipments = pd.read_parquet(
        SILVER_DIR / "tms" / "shipments.parquet"
    )

    warehouse_events = pd.read_parquet(
        SILVER_DIR / "wms" / "warehouse_events.parquet"
    )

    warehouse_expenses = pd.read_parquet(
        SILVER_DIR / "finance" / "warehouse_expenses.parquet"
    )

    shipping_costs = pd.read_parquet(
        SILVER_DIR / "finance" / "shipping_costs.parquet"
    )

    return {
        "warehouses": warehouses,
        "shipments": shipments,
        "warehouse_events": warehouse_events,
        "warehouse_expenses": warehouse_expenses,
        "shipping_costs": shipping_costs,
    }

def calculate_total_orders(
    warehouses: pd.DataFrame,
    shipments: pd.DataFrame
) -> pd.DataFrame:
    """Calculate distinct order count for every warehouse."""

    order_counts = (
        shipments
        .groupby("warehouse_id")
        .agg(
            total_orders=("order_id", "nunique")
        )
        .reset_index()
    )

    result = warehouses[["warehouse_id"]].merge(
        order_counts,
        on="warehouse_id",
        how="left"
    )

    result["total_orders"] = (
        result["total_orders"]
        .fillna(0)
        .astype("int64")
    )

    return result


def calculate_average_processing_time(
    warehouse_events: pd.DataFrame
) -> pd.DataFrame:
    """Calculate average warehouse processing time in minutes."""

    relevant_events = warehouse_events[
        warehouse_events["event_type"].isin([
            "picking_started",
            "carrier_handoff"
        ])
    ]

    event_times = (
        relevant_events
        .pivot_table(
            index=["warehouse_id", "order_id"],
            columns="event_type",
            values="event_timestamp",
            aggfunc="min"
        )
        .reset_index()
    )

    required_columns = [
        "picking_started",
        "carrier_handoff"
    ]

    event_times = event_times.dropna(
        subset=required_columns
    ).copy()

    event_times["processing_time_minutes"] = (
        event_times["carrier_handoff"]
        - event_times["picking_started"]
    ).dt.total_seconds() / 60

    event_times = event_times[
        event_times["processing_time_minutes"] >= 0
    ]

    result = (
        event_times
        .groupby("warehouse_id")
        .agg(
            avg_processing_time_minutes=(
                "processing_time_minutes",
                "mean"
            )
        )
        .reset_index()
    )

    return result





def build_warehouse_performance(
    warehouses: pd.DataFrame,
    shipments: pd.DataFrame,
    warehouse_events: pd.DataFrame,
    warehouse_expenses: pd.DataFrame,
    shipping_costs: pd.DataFrame
) -> pd.DataFrame:

    total_orders = calculate_total_orders(
        warehouses, shipments
    )

    processing_time = calculate_average_processing_time(
        warehouse_events
    )

    operating_cost = calculate_warehouse_operating_cost(
        warehouse_expenses
    )

    shipping_cost = calculate_shipping_cost(
        shipments, shipping_costs
    )

    handoff_rate = calculate_on_time_handoff_rate(
        shipments
    )

    late_handoffs = calculate_late_handoff_count(
        shipments
    )

    result = total_orders.merge(
        processing_time,
        on="warehouse_id",
        how="left"
    )

    result = result.merge(
        operating_cost,
        on="warehouse_id",
        how="left"
    )

    result = result.merge(
        shipping_cost,
        on="warehouse_id",
        how="left"
    )

    result = result.merge(
        handoff_rate,
        on="warehouse_id",
        how="left"
    )

    result = result.merge(
        late_handoffs,
        on="warehouse_id",
        how="left"
    )

    # No completed handoffs means zero completed handoffs
    result["completed_handoffs"] = (
        result["completed_handoffs"]
        .fillna(0)
        .astype("int64")
    )

    result["on_time_handoffs"] = (
        result["on_time_handoffs"]
        .fillna(0)
        .astype("int64")
    )

    result["late_handoff_count"] = (
        result["late_handoff_count"]
        .fillna(0)
        .astype("int64")
    )

    return result




def calculate_warehouse_operating_cost(
    warehouse_expenses: pd.DataFrame
) -> pd.DataFrame:
    """Calculate total operating expenses per warehouse."""

    operating_cost = (
        warehouse_expenses
        .groupby("warehouse_id")
        .agg(
            warehouse_operating_cost=(
                "expense_amount",
                "sum"
            )
        )
        .reset_index()
    )

    return operating_cost



def calculate_shipping_cost(
    shipments: pd.DataFrame,
    shipping_costs: pd.DataFrame
) -> pd.DataFrame:
    """Calculate total shipping costs per warehouse."""

    shipment_warehouse = shipments[
        ["shipment_id", "warehouse_id"]
    ]

    shipping_data = shipping_costs.merge(
        shipment_warehouse,
        on="shipment_id",
        how="inner",
        validate="many_to_one"
    )

    result = (
        shipping_data
        .groupby("warehouse_id")
        .agg(
            total_shipping_cost=(
                "shipping_amount",
                "sum"
            )
        )
        .reset_index()
    )

    return result


def calculate_on_time_handoff_rate(
    shipments: pd.DataFrame
) -> pd.DataFrame:
    """Calculate on-time handoff rate per warehouse."""

    completed_shipments = shipments.dropna(
        subset=[
            "required_handoff_at",
            "actual_handoff_at"
        ]
    ).copy()

    completed_shipments["is_on_time"] = (
        completed_shipments["actual_handoff_at"]
        <= completed_shipments["required_handoff_at"]
    )

    result = (
        completed_shipments
        .groupby("warehouse_id")
        .agg(
            completed_handoffs=("shipment_id", "nunique"),
            on_time_handoffs=("is_on_time", "sum")
        )
        .reset_index()
    )

    result["on_time_handoff_rate"] = (
        result["on_time_handoffs"]
        / result["completed_handoffs"]
        * 100
    )

    return result

def calculate_late_handoff_count(shipments):
    completed = shipments.dropna(
        subset=["required_handoff_at", "actual_handoff_at"]
    ).copy()

    completed["is_late"] = (
        completed["actual_handoff_at"]
        > completed["required_handoff_at"]
    )

    late_handoffs = (
        completed[completed["is_late"]]
        .groupby("warehouse_id")
        .agg(
            late_handoff_count=("shipment_id", "nunique")
        )
        .reset_index()
    )

    return late_handoffs

if __name__ == "__main__":
    data = load_silver_data()

    result = build_warehouse_performance(
        warehouses=data["warehouses"],
        shipments=data["shipments"],
        warehouse_events=data["warehouse_events"],
        warehouse_expenses=data["warehouse_expenses"],
        shipping_costs=data["shipping_costs"]
    )

    # Create Gold output directory
    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    # Save Gold dataset as Parquet
    output_path = GOLD_DIR / "gold_warehouse_performance.parquet"

    result.to_parquet(
        output_path,
        index=False
    )

    print("GOLD WAREHOUSE PERFORMANCE COMPLETED")
    print("=" * 60)
    print(f"Warehouses: {len(result)}")
    print(f"Output: {output_path}")
    print()
    print(result.to_string(index=False))
