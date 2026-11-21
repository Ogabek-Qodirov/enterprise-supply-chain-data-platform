
USE EnterpriseSupplyChainDB;
GO

-- ==========================================
-- TMS: Transportation Management System
-- ==========================================

CREATE SCHEMA tms;
GO

-- 1. Carriers
CREATE TABLE tms.carriers (
    carrier_id VARCHAR(30) PRIMARY KEY,
    carrier_name VARCHAR(150) NOT NULL,
    service_type VARCHAR(50),
    created_at DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
GO

-- 2. Shipments
CREATE TABLE tms.shipments (
    shipment_id VARCHAR(30) PRIMARY KEY,
    order_id VARCHAR(30) NOT NULL,
    carrier_id VARCHAR(30) NOT NULL,
    warehouse_id VARCHAR(30) NOT NULL,
    required_handoff_at DATETIME2 NOT NULL,
    actual_handoff_at DATETIME2,
    expected_delivery_at DATETIME2,
    actual_delivery_at DATETIME2,
    shipment_status VARCHAR(30) NOT NULL,

    CONSTRAINT FK_shipments_orders
        FOREIGN KEY (order_id)
        REFERENCES oms.orders(order_id),

    CONSTRAINT FK_shipments_carriers
        FOREIGN KEY (carrier_id)
        REFERENCES tms.carriers(carrier_id),

    CONSTRAINT FK_shipments_warehouses
        FOREIGN KEY (warehouse_id)
        REFERENCES wms.warehouses(warehouse_id),

    CONSTRAINT UQ_shipments_order
        UNIQUE (order_id)
);
GO

-- 3. Delivery Events
CREATE TABLE tms.delivery_events (
    delivery_event_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    shipment_id VARCHAR(30) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_timestamp DATETIME2 NOT NULL,
    ingested_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    event_location VARCHAR(150),

    CONSTRAINT FK_delivery_events_shipments
        FOREIGN KEY (shipment_id)
        REFERENCES tms.shipments(shipment_id)
);
GO
