CREATE SCHEMA IF NOT EXISTS mart;

CREATE TABLE IF NOT EXISTS mart.revenue_by_month (
    year INTEGER,
    month INTEGER,
    total_orders INTEGER,
    total_revenue NUMERIC,
    total_discount NUMERIC,
    unique_customers INTEGER
);

CREATE TABLE IF NOT EXISTS mart.top_products (
    product_id TEXT,
    product_name TEXT,
    category TEXT,
    total_quantity_sold INTEGER,
    total_revenue NUMERIC,
    order_count INTEGER
);

CREATE TABLE IF NOT EXISTS mart.payment_funnel (
    payment_status TEXT,
    payment_count INTEGER,
    total_amount NUMERIC
);