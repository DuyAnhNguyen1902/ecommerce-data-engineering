CREATE SCHEMA IF NOT EXISTS warehouse;

CREATE TABLE IF NOT EXISTS warehouse.dim_products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price NUMERIC
);

CREATE TABLE IF NOT EXISTS warehouse.fact_orders (
    order_id TEXT PRIMARY KEY,
    user_id TEXT,
    created_at TIMESTAMPTZ,
    final_total NUMERIC,
    discount_value NUMERIC,
    status TEXT,
    payment_method TEXT
);

CREATE TABLE IF NOT EXISTS warehouse.fact_order_items (
    order_id TEXT,
    product_id TEXT,
    variant_id TEXT,
    quantity INTEGER,
    price NUMERIC,
    line_total NUMERIC,
    PRIMARY KEY (order_id, product_id, variant_id)
);

CREATE TABLE IF NOT EXISTS warehouse.fact_payments (
    payment_id TEXT PRIMARY KEY,
    order_id TEXT,
    payment_status TEXT,
    amount_vnd NUMERIC,
    paid_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS warehouse.fact_reviews (
    review_id TEXT PRIMARY KEY,
    product_id TEXT,
    user_id TEXT,
    rating NUMERIC,
    comment TEXT,
    created_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS warehouse.fact_product_sales (
    product_id TEXT,
    month INTEGER,
    year INTEGER,
    quantity_sold INTEGER,
    revenue NUMERIC,
    PRIMARY KEY (product_id, month, year)
);

CREATE TABLE IF NOT EXISTS warehouse.dim_inventory_status (
    product_id TEXT,
    product_name TEXT,
    variant_id TEXT,
    stock INTEGER,
    is_low_stock BOOLEAN,
    created_at TIMESTAMPTZ,
    PRIMARY KEY (product_id, variant_id, created_at)
);