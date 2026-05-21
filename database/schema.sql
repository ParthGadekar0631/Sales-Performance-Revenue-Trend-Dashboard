-- Sales Performance & Revenue Trend Dashboard schema
-- SQLite-compatible analytical schema for cleaned transactions and KPI marts.

DROP TABLE IF EXISTS sales_transactions;
DROP TABLE IF EXISTS monthly_revenue_summary;
DROP TABLE IF EXISTS product_performance;
DROP TABLE IF EXISTS category_performance;
DROP TABLE IF EXISTS regional_performance;
DROP TABLE IF EXISTS sales_channel_performance;
DROP TABLE IF EXISTS dashboard_kpis;

CREATE TABLE sales_transactions (
    transaction_id TEXT PRIMARY KEY,
    transaction_date TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price > 0),
    discount REAL NOT NULL CHECK (discount >= 0 AND discount <= 0.75),
    region TEXT NOT NULL,
    sales_channel TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    gross_revenue REAL NOT NULL,
    discount_amount REAL NOT NULL,
    net_revenue REAL NOT NULL,
    average_order_value REAL NOT NULL,
    transaction_month TEXT NOT NULL,
    transaction_year INTEGER NOT NULL,
    monthly_sales TEXT NOT NULL,
    yearly_sales INTEGER NOT NULL
);

CREATE TABLE monthly_revenue_summary (
    transaction_month TEXT PRIMARY KEY,
    total_revenue REAL NOT NULL,
    gross_revenue REAL NOT NULL,
    discount_amount REAL NOT NULL,
    total_orders INTEGER NOT NULL,
    total_units_sold INTEGER NOT NULL,
    average_transaction_value REAL NOT NULL,
    monthly_growth_pct REAL NOT NULL,
    revenue_rank INTEGER NOT NULL
);

CREATE TABLE product_performance (
    product_id TEXT NOT NULL,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    total_revenue REAL NOT NULL,
    gross_revenue REAL NOT NULL,
    discount_amount REAL NOT NULL,
    total_orders INTEGER NOT NULL,
    total_units_sold INTEGER NOT NULL,
    average_transaction_value REAL NOT NULL,
    revenue_contribution_pct REAL NOT NULL,
    revenue_rank INTEGER NOT NULL
);

CREATE TABLE category_performance (
    category TEXT PRIMARY KEY,
    total_revenue REAL NOT NULL,
    gross_revenue REAL NOT NULL,
    discount_amount REAL NOT NULL,
    total_orders INTEGER NOT NULL,
    total_units_sold INTEGER NOT NULL,
    average_transaction_value REAL NOT NULL,
    revenue_contribution_pct REAL NOT NULL,
    revenue_rank INTEGER NOT NULL
);

CREATE TABLE regional_performance (
    region TEXT PRIMARY KEY,
    total_revenue REAL NOT NULL,
    gross_revenue REAL NOT NULL,
    discount_amount REAL NOT NULL,
    total_orders INTEGER NOT NULL,
    total_units_sold INTEGER NOT NULL,
    average_transaction_value REAL NOT NULL,
    revenue_contribution_pct REAL NOT NULL,
    revenue_rank INTEGER NOT NULL
);

CREATE TABLE sales_channel_performance (
    sales_channel TEXT PRIMARY KEY,
    total_revenue REAL NOT NULL,
    gross_revenue REAL NOT NULL,
    discount_amount REAL NOT NULL,
    total_orders INTEGER NOT NULL,
    total_units_sold INTEGER NOT NULL,
    average_transaction_value REAL NOT NULL,
    revenue_contribution_pct REAL NOT NULL,
    revenue_rank INTEGER NOT NULL
);

CREATE TABLE dashboard_kpis (
    kpi_name TEXT PRIMARY KEY,
    kpi_value REAL NOT NULL,
    unit TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE INDEX idx_sales_transaction_date ON sales_transactions(transaction_date);
CREATE INDEX idx_sales_category ON sales_transactions(category);
CREATE INDEX idx_sales_region ON sales_transactions(region);
CREATE INDEX idx_sales_channel ON sales_transactions(sales_channel);
CREATE INDEX idx_sales_product ON sales_transactions(product_id);

