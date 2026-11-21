
USE EnterpriseSupplyChainDB;
GO

-- ==========================================
-- WMS: Warehouse Management System
-- ==========================================

CREATE SCHEMA wms;
GO

-- 1. Warehouses
CREATE TABLE wms.warehouses (
    warehouse_id VARCHAR(30) PRIMARY KEY,
    warehouse_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    warehouse_capacity INT NOT NULL
        CHECK (warehouse_capacity > 0),
    created_at DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
GO

-- 2. Employees
CREATE TABLE wms.employees (
    employee_id VARCHAR(30) PRIMARY KEY,
    warehouse_id VARCHAR(30) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    job_title VARCHAR(100),
    hire_date DATE,

    CONSTRAINT FK_employees_warehouses
        FOREIGN KEY (warehouse_id)
        REFERENCES wms.warehouses(warehouse_id)
);
GO

-- 3. Warehouse Events
CREATE TABLE wms.warehouse_events (
    event_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    order_id VARCHAR(30) NOT NULL,
    warehouse_id VARCHAR(30) NOT NULL,
    employee_id VARCHAR(30),
    event_type VARCHAR(50) NOT NULL,
    event_timestamp DATETIME2 NOT NULL,
    ingested_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

    CONSTRAINT FK_warehouse_events_orders
        FOREIGN KEY (order_id)
        REFERENCES oms.orders(order_id),

    CONSTRAINT FK_warehouse_events_warehouses
        FOREIGN KEY (warehouse_id)
        REFERENCES wms.warehouses(warehouse_id),

    CONSTRAINT FK_warehouse_events_employees
        FOREIGN KEY (employee_id)
        REFERENCES wms.employees(employee_id)
);
GO

-- 4. Inventory
CREATE TABLE wms.inventory (
    inventory_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    warehouse_id VARCHAR(30) NOT NULL,
    product_id VARCHAR(30) NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0),
    last_updated_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

    CONSTRAINT FK_inventory_warehouses
        FOREIGN KEY (warehouse_id)
        REFERENCES wms.warehouses(warehouse_id),

    CONSTRAINT FK_inventory_products
        FOREIGN KEY (product_id)
        REFERENCES oms.products(product_id),

    CONSTRAINT UQ_inventory_warehouse_product
        UNIQUE (warehouse_id, product_id)
);
GO
