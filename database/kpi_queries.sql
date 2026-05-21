-- Executive KPI summary
SELECT
    ROUND(SUM(net_revenue), 2) AS total_revenue,
    COUNT(DISTINCT transaction_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    ROUND(AVG(net_revenue), 2) AS average_transaction_value
FROM sales_transactions;

-- Monthly revenue and growth
WITH monthly AS (
    SELECT
        transaction_month,
        ROUND(SUM(net_revenue), 2) AS total_revenue,
        COUNT(DISTINCT transaction_id) AS total_orders,
        SUM(quantity) AS total_units_sold,
        ROUND(AVG(net_revenue), 2) AS average_transaction_value
    FROM sales_transactions
    GROUP BY transaction_month
)
SELECT
    transaction_month,
    total_revenue,
    total_orders,
    total_units_sold,
    average_transaction_value,
    ROUND(
        COALESCE(
            (total_revenue - LAG(total_revenue) OVER (ORDER BY transaction_month))
            / NULLIF(LAG(total_revenue) OVER (ORDER BY transaction_month), 0) * 100,
            0
        ),
        2
    ) AS monthly_growth_pct
FROM monthly
ORDER BY transaction_month;

-- Revenue by product
SELECT
    product_id,
    product_name,
    category,
    ROUND(SUM(net_revenue), 2) AS total_revenue,
    COUNT(DISTINCT transaction_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    ROUND(AVG(net_revenue), 2) AS average_transaction_value
FROM sales_transactions
GROUP BY product_id, product_name, category
ORDER BY total_revenue DESC;

-- Revenue by category
SELECT
    category,
    ROUND(SUM(net_revenue), 2) AS total_revenue,
    COUNT(DISTINCT transaction_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    ROUND(AVG(net_revenue), 2) AS average_transaction_value
FROM sales_transactions
GROUP BY category
ORDER BY total_revenue DESC;

-- Revenue by region
SELECT
    region,
    ROUND(SUM(net_revenue), 2) AS total_revenue,
    COUNT(DISTINCT transaction_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    ROUND(AVG(net_revenue), 2) AS average_transaction_value
FROM sales_transactions
GROUP BY region
ORDER BY total_revenue DESC;

-- Revenue by sales channel
SELECT
    sales_channel,
    ROUND(SUM(net_revenue), 2) AS total_revenue,
    COUNT(DISTINCT transaction_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    ROUND(AVG(net_revenue), 2) AS average_transaction_value
FROM sales_transactions
GROUP BY sales_channel
ORDER BY total_revenue DESC;

-- Top products
SELECT product_name, category, total_revenue, total_units_sold, revenue_rank
FROM product_performance
ORDER BY revenue_rank
LIMIT 10;

-- Top categories
SELECT category, total_revenue, revenue_contribution_pct, revenue_rank
FROM category_performance
ORDER BY revenue_rank;

-- Highest revenue months
SELECT transaction_month, total_revenue, monthly_growth_pct, revenue_rank
FROM monthly_revenue_summary
ORDER BY total_revenue DESC
LIMIT 10;

-- Best performing regions
SELECT region, total_revenue, revenue_contribution_pct, revenue_rank
FROM regional_performance
ORDER BY revenue_rank;

