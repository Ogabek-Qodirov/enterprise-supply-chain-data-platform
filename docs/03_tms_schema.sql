
-- =========================================
-- TMS: Transportation Management System
-- =========================================

CREATE TABLE carriers (
    carrier_id VARCHAR(30) PRIMARY KEY,
    carrier_name VARCHAR(150) NOT NULL,
    service_type VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE shipments (
    shipment_id VARCHAR(30) PRIMARY KEY,
    order_id VARCHAR(30) NOT NULL,
    carrier_id VARCHAR(30) NOT NULL,
    warehouse_id VARCHAR(30) NOT NULL,
    required_handoff_at TIMESTAMP NOT NULL,
    actual_handoff_at TIMESTAMP,
    expected_delivery_at TIMESTAMP,
    actual_delivery_at TIMESTAMP,
    shipment_status VARCHAR(30) NOT NULL,

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (carrier_id)
        REFERENCES carriers(carrier_id),

    FOREIGN KEY (warehouse_id)
        REFERENCES warehouses(warehouse_id),

    UNIQUE (order_id)
);

CREATE TABLE delivery_events (
    delivery_event_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    shipment_id VARCHAR(30) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    ingested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    event_location VARCHAR(150),

    FOREIGN KEY (shipment_id)
        REFERENCES shipments(shipment_id)
);
