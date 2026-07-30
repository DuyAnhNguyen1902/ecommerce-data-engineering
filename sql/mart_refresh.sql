-- ============================================================
-- FULL REFRESH: WAREHOUSE -> MART
--
-- This script must run inside one database transaction.
-- If any INSERT fails, Python will roll back the entire refresh.
-- ============================================================


-- ============================================================
-- CLEAR CURRENT MART DATA
-- ============================================================

TRUNCATE TABLE
    mart.revenue_by_month,
    mart.top_products,
    mart.payment_funnel;


-- ============================================================
-- 1. REVENUE BY MONTH
-- Only completed orders are included in revenue KPIs.
-- ============================================================

INSERT INTO mart.revenue_by_month (
    year,
    month,
    total_orders,
    total_revenue,
    total_discount,
    unique_customers
)
SELECT
    EXTRACT(YEAR FROM created_at)::INTEGER AS year,
    EXTRACT(MONTH FROM created_at)::INTEGER AS month,
    COUNT(DISTINCT order_id) AS total_orders,
    COALESCE(SUM(final_total), 0)::NUMERIC(20, 2)
        AS total_revenue,
    COALESCE(SUM(discount_value), 0)::NUMERIC(20, 2)
        AS total_discount,
    COUNT(DISTINCT user_id) AS unique_customers
FROM warehouse.fact_orders
WHERE
    created_at IS NOT NULL
    AND LOWER(TRIM(status)) = 'completed'
GROUP BY
    EXTRACT(YEAR FROM created_at),
    EXTRACT(MONTH FROM created_at);


-- ============================================================
-- 2. TOP PRODUCTS
-- Only products belonging to completed orders are included.
-- ============================================================

INSERT INTO mart.top_products (
    product_id,
    product_name,
    category,
    total_quantity_sold,
    total_revenue,
    order_count
)
SELECT
    i.product_id,
    COALESCE(p.product_name, 'Unknown Product')
        AS product_name,
    COALESCE(p.category, 'Unknown Category')
        AS category,
    COALESCE(SUM(i.quantity), 0)
        AS total_quantity_sold,
    COALESCE(SUM(i.line_total), 0)::NUMERIC(20, 2)
        AS total_revenue,
    COUNT(DISTINCT i.order_id)
        AS order_count
FROM warehouse.fact_order_items AS i
INNER JOIN warehouse.fact_orders AS o
    ON i.order_id = o.order_id
LEFT JOIN warehouse.dim_products AS p
    ON i.product_id = p.product_id
WHERE
    LOWER(TRIM(o.status)) = 'completed'
GROUP BY
    i.product_id,
    p.product_name,
    p.category;


-- ============================================================
-- 3. PAYMENT FUNNEL
-- NULL or blank statuses are grouped as UNKNOWN.
-- ============================================================

INSERT INTO mart.payment_funnel (
    payment_status,
    payment_count,
    total_amount
)
SELECT
    COALESCE(
        NULLIF(UPPER(TRIM(payment_status)), ''),
        'UNKNOWN'
    ) AS payment_status,
    COUNT(*) AS payment_count,
    COALESCE(SUM(amount_vnd), 0)::NUMERIC(20, 2)
        AS total_amount
FROM warehouse.fact_payments
GROUP BY
    COALESCE(
        NULLIF(UPPER(TRIM(payment_status)), ''),
        'UNKNOWN'
    );