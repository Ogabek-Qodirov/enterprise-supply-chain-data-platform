
USE EnterpriseSupplyChainDB;
GO

-- ==========================================
-- OMS: Order Management System
-- ==========================================

CREATE SCHEMA oms;
GO

-- 1. Customers
CREATE TABLE oms.customers (
    customer_id VARCHAR(30) PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE,
    created_at DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
GO

-- 2. Products
CREATE TABLE oms.products (
    product_id VARCHAR(30) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    unit_price DECIMAL(12, 2) NOT NULL
        CHECK (unit_price >= 0)
);
GO

-- 3. Orders
CREATE TABLE oms.orders (
    order_id VARCHAR(30) PRIMARY KEY,
    customer_id VARCHAR(30) NOT NULL,
    order_status VARCHAR(30) NOT NULL,
    order_timestamp DATETIME2 NOT NULL,

    CONSTRAINT FK_orders_customers
        FOREIGN KEY (customer_id)
        REFERENCES oms.customers(customer_id)
);
GO

-- 4. Order Items
CREATE TABLE oms.order_items (
    order_item_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    order_id VARCHAR(30) NOT NULL,
    product_id VARCHAR(30) NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(12, 2) NOT NULL
        CHECK (unit_price >= 0),

    CONSTRAINT FK_order_items_orders
        FOREIGN KEY (order_id)
        REFERENCES oms.orders(order_id),

    CONSTRAINT FK_order_items_products
        FOREIGN KEY (product_id)
        REFERENCES oms.products(product_id),

    CONSTRAINT UQ_order_items_order_product
        UNIQUE (order_id, product_id)
);
GO
