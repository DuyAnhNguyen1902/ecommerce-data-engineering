-- ============================================================
-- MART LAYER INITIALIZATION
-- ============================================================

CREATE SCHEMA IF NOT EXISTS mart;


-- ============================================================
-- 1. REVENUE BY MONTH
-- Grain: one row per year and month
-- ============================================================

CREATE TABLE IF NOT EXISTS mart.revenue_by_month (
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    total_orders BIGINT NOT NULL,
    total_revenue NUMERIC(20, 2) NOT NULL,
    total_discount NUMERIC(20, 2) NOT NULL,
    unique_customers BIGINT NOT NULL,

    PRIMARY KEY (year, month),

    CHECK (month BETWEEN 1 AND 12),
    CHECK (total_orders >= 0),
    CHECK (total_revenue >= 0),
    CHECK (total_discount >= 0),
    CHECK (unique_customers >= 0)
);


-- ============================================================
-- 2. TOP PRODUCTS
-- Grain: one row per product
-- ============================================================

CREATE TABLE IF NOT EXISTS mart.top_products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    total_quantity_sold BIGINT NOT NULL,
    total_revenue NUMERIC(20, 2) NOT NULL,
    order_count BIGINT NOT NULL,

    CHECK (total_quantity_sold >= 0),
    CHECK (total_revenue >= 0),
    CHECK (order_count >= 0)
);


-- ============================================================
-- 3. PAYMENT FUNNEL
-- Grain: one row per payment status
-- ============================================================

CREATE TABLE IF NOT EXISTS mart.payment_funnel (
    payment_status TEXT PRIMARY KEY,
    payment_count BIGINT NOT NULL,
    total_amount NUMERIC(20, 2) NOT NULL,

    CHECK (payment_count >= 0),
    CHECK (total_amount >= 0)
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_mart_top_products_revenue
    ON mart.top_products (total_revenue DESC);

CREATE INDEX IF NOT EXISTS idx_mart_top_products_category
    ON mart.top_products (category);

CREATE INDEX IF NOT EXISTS idx_mart_payment_funnel_amount
    ON mart.payment_funnel (total_amount DESC);