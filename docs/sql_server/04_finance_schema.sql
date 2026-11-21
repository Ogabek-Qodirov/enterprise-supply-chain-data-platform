
USE EnterpriseSupplyChainDB;
GO

-- ==========================================
-- Finance: Financial Management System
-- ==========================================

CREATE SCHEMA finance;
GO

-- 1. Order Revenue
CREATE TABLE finance.order_revenue (
    revenue_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    order_id VARCHAR(30) NOT NULL,
    revenue_amount DECIMAL(12, 2) NOT NULL
        CHECK (revenue_amount >= 0),
    recognized_at DATETIME2 NOT NULL,

    CONSTRAINT FK_order_revenue_orders
        FOREIGN KEY (order_id)
        REFERENCES oms.orders(order_id),

    CONSTRAINT UQ_order_revenue_order
        UNIQUE (order_id)
);
GO

-- 2. Warehouse Expenses
CREATE TABLE finance.warehouse_expenses (
    expense_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    warehouse_id VARCHAR(30) NOT NULL,
    expense_category VARCHAR(100) NOT NULL,
    expense_amount DECIMAL(12, 2) NOT NULL
        CHECK (expense_amount >= 0),
    expense_timestamp DATETIME2 NOT NULL,
    description VARCHAR(500),

    CONSTRAINT FK_warehouse_expenses_warehouses
        FOREIGN KEY (warehouse_id)
        REFERENCES wms.warehouses(warehouse_id)
);
GO

-- 3. Shipping Costs
CREATE TABLE finance.shipping_costs (
    shipping_cost_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    shipment_id VARCHAR(30) NOT NULL,
    shipping_amount DECIMAL(12, 2) NOT NULL
        CHECK (shipping_amount >= 0),
    recorded_at DATETIME2 NOT NULL,
    description VARCHAR(500),

    CONSTRAINT FK_shipping_costs_shipments
        FOREIGN KEY (shipment_id)
        REFERENCES tms.shipments(shipment_id)
);
GO
