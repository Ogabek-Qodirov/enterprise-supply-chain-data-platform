# SQL Server Source Database

This directory contains the SQL Server (T-SQL) scripts used to create the source database for the Enterprise Supply Chain Data Platform.

## Database

- **Database name:** `EnterpriseSupplyChainDB`
- **Database engine:** Microsoft SQL Server
- **SQL client:** SQL Server Management Studio (SSMS)

## Source Systems

| Schema | Description |
|---|---|
| `oms` | Order Management System |
| `wms` | Warehouse Management System |
| `tms` | Transportation Management System |
| `finance` | Financial Management System |

## Schema Scripts

1. `01_oms_schema.sql` — Customers, products, orders and order items.
2. `02_wms_schema.sql` — Warehouses, employees, inventory and warehouse events.
3. `03_tms_schema.sql` — Carriers, shipments and delivery events.
4. `04_finance_schema.sql` — Order revenue, warehouse expenses and shipping costs.

## Execution Order

Execute the scripts in the following order:

1. OMS
2. WMS
3. TMS
4. Finance

Each script creates its schema and tables. The database itself must already exist.

## Notes

- These scripts use SQL Server T-SQL syntax.
- Foreign key constraints maintain relationships between source systems.
- `DATETIME2` is used for event timestamps.
- `IDENTITY` generates numeric identifiers for event and transaction records.
- Sample data is managed separately from schema definitions.