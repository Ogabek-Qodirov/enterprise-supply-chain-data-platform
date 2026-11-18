
-- =========================================
-- WMS: Warehouse Management System
-- =========================================

CREATE TABLE warehouses (
    warehouse_id VARCHAR(30) PRIMARY KEY,
    warehouse_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    warehouse_capacity INTEGER NOT NULL CHECK (warehouse_capacity > 0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE employees (
    employee_id VARCHAR(30) PRIMARY KEY,
    warehouse_id VARCHAR(30) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    job_title VARCHAR(100),
    hire_date DATE,

    FOREIGN KEY (warehouse_id)
        REFERENCES warehouses(warehouse_id)
);

CREATE TABLE warehouse_events (
    event_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id VARCHAR(30) NOT NULL,
    warehouse_id VARCHAR(30) NOT NULL,
    employee_id VARCHAR(30),
    event_type VARCHAR(50) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    ingested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (warehouse_id)
        REFERENCES warehouses(warehouse_id),

    FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);

CREATE TABLE inventory (
    inventory_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    warehouse_id VARCHAR(30) NOT NULL,
    product_id VARCHAR(30) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    last_updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (warehouse_id)
        REFERENCES warehouses(warehouse_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    UNIQUE (warehouse_id, product_id)
);
