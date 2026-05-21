# Tableau Dashboard Requirements

## 1. Executive KPI Dashboard

Purpose: give executives a fast revenue health overview.

Required visuals:
- KPI tiles for Total Revenue, Latest Monthly Growth %, Average Transaction Value, Total Orders, and Total Units Sold.
- Monthly revenue trend line.
- Top region and top sales channel summary.

Primary data sources:
- `dashboard_kpis.csv`
- `monthly_revenue_summary.csv`
- `regional_performance.csv`
- `sales_channel_performance.csv`

## 2. Revenue Trend Dashboard

Purpose: monitor revenue growth, seasonality, and monthly performance changes.

Required visuals:
- Monthly revenue line chart.
- Monthly growth percentage bar chart.
- Highest revenue month ranking.
- Rolling context using `transaction_month`.

Primary data source:
- `monthly_revenue_summary.csv`

## 3. Product Performance Dashboard

Purpose: identify products that drive revenue and volume.

Required visuals:
- Top 10 products by revenue.
- Units sold by product.
- Revenue contribution percentage.
- Product rank table with category context.

Primary data source:
- `product_performance.csv`

## 4. Category Dashboard

Purpose: compare category-level performance and revenue share.

Required visuals:
- Revenue by category bar chart.
- Category contribution donut or treemap.
- Total orders and average transaction value by category.

Primary data source:
- `category_performance.csv`

## 5. Regional Dashboard

Purpose: compare geographic performance for sales planning.

Required visuals:
- Revenue by region.
- Orders and units by region.
- Regional revenue contribution percentage.

Primary data source:
- `regional_performance.csv`

## 6. Sales Channel Dashboard

Purpose: compare online, retail, wholesale, partner, and inside-sales performance.

Required visuals:
- Revenue by sales channel.
- Channel revenue share.
- Average transaction value by sales channel.
- Order count by sales channel.

Primary data source:
- `sales_channel_performance.csv`

