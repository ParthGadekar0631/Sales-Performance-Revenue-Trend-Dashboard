# Tableau Data Dictionary

## cleaned_sales.csv

| Field | Description |
| --- | --- |
| transaction_id | Unique transaction identifier |
| transaction_date | Sales transaction date |
| customer_id | Customer identifier |
| product_id | Product identifier |
| product_name | Product display name |
| category | Normalized product category |
| quantity | Units sold |
| unit_price | Unit selling price |
| discount | Discount rate applied to the transaction |
| region | Sales region |
| sales_channel | Sales channel |
| payment_method | Payment method |
| gross_revenue | Quantity multiplied by unit price |
| discount_amount | Gross revenue multiplied by discount |
| net_revenue | Gross revenue less discount amount |
| average_order_value | Transaction-level net revenue |
| transaction_month | Year-month reporting period |
| transaction_year | Reporting year |
| monthly_sales | Month label for Tableau filtering |
| yearly_sales | Year label for Tableau filtering |

## monthly_revenue_summary.csv

| Field | Description |
| --- | --- |
| transaction_month | Monthly reporting period |
| total_revenue | Net revenue for the month |
| gross_revenue | Gross revenue for the month |
| discount_amount | Discount value for the month |
| total_orders | Unique order count |
| total_units_sold | Units sold |
| average_transaction_value | Average net revenue per order |
| monthly_growth_pct | Month-over-month revenue growth |
| revenue_rank | Rank by monthly revenue |

## Performance CSVs

The product, category, regional, and sales channel performance exports use consistent KPI fields:

| Field | Description |
| --- | --- |
| total_revenue | Net revenue for the segment |
| gross_revenue | Gross revenue before discount |
| discount_amount | Discount value for the segment |
| total_orders | Unique order count |
| total_units_sold | Units sold |
| average_transaction_value | Average net revenue per order |
| revenue_contribution_pct | Segment share of total revenue |
| revenue_rank | Revenue rank within the export |

## dashboard_kpis.csv

| Field | Description |
| --- | --- |
| kpi_name | Executive KPI name |
| kpi_value | Numeric KPI value |
| unit | Unit of measure |
| description | Business definition |

