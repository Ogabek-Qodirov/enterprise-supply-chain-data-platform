&#x20;# Data Model Design



\## 1. Purpose



This document defines the initial data model for the Enterprise Supply Chain Data Platform.



The platform integrates OMS, WMS, TMS, and Finance data to support warehouse performance analysis, delivery monitoring, and financial reporting.



\## 2. Source Systems



\- OMS: Order Management System

\- WMS: Warehouse Management System

\- TMS: Transportation Management System

\- Finance: Financial Management System



\## 3. Warehouse Events Table



\### Table: `warehouse\_events`



\*\*Grain:\*\* One row represents one event associated with one order at a specific point in time.



| Column | Description |

|---|---|

| event\_id | Unique event identifier |

| order\_id | Identifier of the related order |

| warehouse\_id | Identifier of the warehouse |

| employee\_id | Employee associated with the event, if applicable |

| event\_type | Type of warehouse activity |

| event\_timestamp | Time the event actually occurred |

| ingested\_at | Time the platform received the event |



\### Example Events



An order may generate multiple events:



\- picking\_started

\- picking\_completed

\- packing\_started

\- packing\_completed

\- quality\_check\_passed

\- carrier\_handoff



Each event is stored as a separate row.



\## 4. Data Modeling Principles



1\. Every event must have a unique identifier.

2\. Events belonging to the same order share the same `order\_id`.

3\. Event timestamps must preserve the actual occurrence time.

4\. Ingestion timestamps must be stored separately.

5\. Multiple events must not be collapsed into one order record.

6\. Source data should be preserved before transformation.



\## 5. Future Considerations



\- Handling late-arriving events.

\- Handling duplicate events.

\- Maintaining event history.

\- Validating foreign-key relationships.

\- Supporting incremental data ingestion.

