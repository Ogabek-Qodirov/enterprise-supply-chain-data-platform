
# Gold Layer Design

## Business Objective

The Gold Layer provides business-ready datasets for
supply chain performance analysis.

The first Gold dataset is designed to evaluate
warehouse operational performance.

## Dataset

Name: gold_warehouse_performance

Grain: One row per warehouse.

Source systems:
- OMS
- WMS
- TMS
- Finance

## Business Metrics

- Total Orders
- Completed Orders
- On-time Handoff Rate
- Average Processing Time
- Warehouse Operating Cost
- Shipping Cost
- Warehouse-caused Delay Count

## Business Rules

- A warehouse is identified by warehouse_id.
- Orders are associated with warehouses through shipments.
- Handoff performance uses required_handoff_at
  and actual_handoff_at.
- Pending shipments are excluded from the on-time
  handoff denominator.
- Processing time is calculated from warehouse events.
- Warehouse operating expenses are aggregated
  from Finance data.
- Shipping costs are associated with shipments.
- Silver data remains immutable.
- Gold outputs are stored as Parquet.

## Data Quality

- One row per warehouse.
- warehouse_id must be unique and non-null.
- KPI values must follow documented business rules.
- Missing source values must not be silently replaced.
