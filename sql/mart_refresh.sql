TRUNCATE TABLE mart.revenue_by_month;
TRUNCATE TABLE mart.top_products;
TRUNCATE TABLE mart.payment_funnel;

INSERT INTO mart.revenue_by_month (
    year,
    month,
    total_orders,
    total_revenue,
    total_discount,
    unique_customers
)
SELECT
    EXTRACT(YEAR FROM created_at)::INT AS year,
    EXTRACT(MONTH FROM created_at)::INT AS month,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(final_total) AS total_revenue,
    SUM(discount_value) AS total_discount,
    COUNT(DISTINCT user_id) AS unique_customers
FROM warehouse.fact_orders
GROUP BY 1, 2
ORDER BY 1, 2;


INSERT INTO mart.top_products (
    product_id,
    product_name,
    category,
    total_quantity_sold,
    total_revenue,
    order_count
)
SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(i.quantity) AS total_quantity_sold,
    SUM(i.line_total) AS total_revenue,
    COUNT(DISTINCT i.order_id) AS order_count
FROM warehouse.fact_order_items i
LEFT JOIN warehouse.dim_products p
    ON i.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY total_revenue DESC;


INSERT INTO mart.payment_funnel (
    payment_status,
    payment_count,
    total_amount
)
SELECT
    payment_status,
    COUNT(*) AS payment_count,
    SUM(amount_vnd) AS total_amount
FROM warehouse.fact_payments
GROUP BY payment_status
ORDER BY total_amount DESC;