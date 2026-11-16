\# Enterprise Supply Chain Data Platform



\## 1. Business Overview



A fictional logistics company operates five warehouses and works with multiple delivery partners.



The company receives thousands of customer orders through its Order Management System (OMS). Warehouse operations are managed through a Warehouse Management System (WMS), while deliveries are tracked through a Transportation Management System (TMS).



Currently, management does not have a unified view of operational performance across all warehouses.



The purpose of this platform is to integrate data from different business systems and transform it into reliable information for management decisions.



\## 2. Business Problems



Management needs answers to the following questions:



1\. Which warehouse has the highest operational performance?

2\. Which warehouse has the lowest performance?

3\. Which warehouses process orders most efficiently?

4\. Which delivery partners cause the most delays?

5\. How much does each warehouse spend per fulfilled order?

6\. What percentage of late deliveries are caused by warehouse operations rather than delivery partners?

7\. Which operational areas require improvement?



\## 3. Data Sources



| Source | Description | Important Data |

|---|---|---|

| OMS | Order Management System | Orders, customers, products, order timestamps |

| WMS | Warehouse Management System | Picking, packing, inventory, warehouse events |

| TMS | Transportation Management System | Carriers, shipments, delivery timestamps |

| Finance | Financial System | Revenue, operating expenses, shipping costs |



The systems will be connected through shared identifiers such as `order\_id`, `warehouse\_id`, and `carrier\_id`.



\## 4. Key Performance Indicators (KPIs)



\- On-time fulfillment rate

\- Average order processing time

\- On-time carrier handoff rate

\- Picking accuracy

\- Warehouse damage rate

\- Warehouse-caused delay rate

\- Carrier-caused delay rate

\- Cost per fulfilled order

\- Inventory turnover



\## 5. Expected Business Outcomes



The platform should provide management with:



\- A unified view of warehouse performance.

\- Comparisons between warehouses using consistent KPIs.

\- Visibility into operational bottlenecks.

\- Identification of delivery delay root causes.

\- Financial performance analysis.

\- Reliable data for evidence-based business decisions.



\## 6. Decision-Making Principles



The platform will provide analytical evidence rather than automatically making business decisions.



Warehouse closure, employee evaluation, or operational restructuring must consider multiple factors, including costs, demand, capacity, location, customer experience, and operational context.



\## 7. Initial Project Scope



The first version will focus on:



1\. Designing realistic source data.

2\. Building batch data ingestion pipelines.

3\. Storing raw data in a Bronze layer.

4\. Cleaning and validating data in a Silver layer.

5\. Producing business-ready Gold datasets.

6\. Calculating warehouse performance KPIs.

7\. Making analytical results available for reporting.

