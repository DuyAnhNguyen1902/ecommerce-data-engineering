-- ============================================================
-- INCREMENTAL LOAD: RAW -> WAREHOUSE
-- Uses UPSERT to make the load idempotent.
-- ============================================================


-- ============================================================
-- 1. DIM_PRODUCTS
-- ============================================================

INSERT INTO warehouse.dim_products (
    product_id,
    product_name,
    category,
    price
)
SELECT
    product_id,
    product_name,
    category,
    price::NUMERIC
FROM raw.dim_products
ON CONFLICT (product_id)
DO UPDATE SET
    product_name = EXCLUDED.product_name,
    category = EXCLUDED.category,
    price = EXCLUDED.price
WHERE (
    warehouse.dim_products.product_name,
    warehouse.dim_products.category,
    warehouse.dim_products.price
) IS DISTINCT FROM (
    EXCLUDED.product_name,
    EXCLUDED.category,
    EXCLUDED.price
);


-- ============================================================
-- 2. FACT_ORDERS
-- ============================================================

INSERT INTO warehouse.fact_orders (
    order_id,
    user_id,
    created_at,
    final_total,
    discount_value,
    status,
    payment_method
)
SELECT
    order_id,
    user_id,
    created_at::TIMESTAMPTZ,
    final_total::NUMERIC,
    discount_value::NUMERIC,
    status,
    payment_method
FROM raw.fact_orders
ON CONFLICT (order_id)
DO UPDATE SET
    user_id = EXCLUDED.user_id,
    created_at = EXCLUDED.created_at,
    final_total = EXCLUDED.final_total,
    discount_value = EXCLUDED.discount_value,
    status = EXCLUDED.status,
    payment_method = EXCLUDED.payment_method
WHERE (
    warehouse.fact_orders.user_id,
    warehouse.fact_orders.created_at,
    warehouse.fact_orders.final_total,
    warehouse.fact_orders.discount_value,
    warehouse.fact_orders.status,
    warehouse.fact_orders.payment_method
) IS DISTINCT FROM (
    EXCLUDED.user_id,
    EXCLUDED.created_at,
    EXCLUDED.final_total,
    EXCLUDED.discount_value,
    EXCLUDED.status,
    EXCLUDED.payment_method
);


-- ============================================================
-- 3. FACT_ORDER_ITEMS
-- ============================================================

INSERT INTO warehouse.fact_order_items (
    order_id,
    product_id,
    variant_id,
    quantity,
    price,
    line_total
)
SELECT
    order_id,
    product_id,
    variant_id,
    quantity::INTEGER,
    price::NUMERIC,
    line_total::NUMERIC
FROM raw.fact_order_items
ON CONFLICT (order_id, product_id, variant_id)
DO UPDATE SET
    quantity = EXCLUDED.quantity,
    price = EXCLUDED.price,
    line_total = EXCLUDED.line_total
WHERE (
    warehouse.fact_order_items.quantity,
    warehouse.fact_order_items.price,
    warehouse.fact_order_items.line_total
) IS DISTINCT FROM (
    EXCLUDED.quantity,
    EXCLUDED.price,
    EXCLUDED.line_total
);


-- ============================================================
-- 4. FACT_PAYMENTS
-- ============================================================

INSERT INTO warehouse.fact_payments (
    payment_id,
    order_id,
    payment_status,
    amount_vnd,
    paid_at,
    created_at
)
SELECT
    payment_id,
    order_id,
    payment_status,
    amount_vnd::NUMERIC,
    paid_at::TIMESTAMPTZ,
    created_at::TIMESTAMPTZ
FROM raw.fact_payments
ON CONFLICT (payment_id)
DO UPDATE SET
    order_id = EXCLUDED.order_id,
    payment_status = EXCLUDED.payment_status,
    amount_vnd = EXCLUDED.amount_vnd,
    paid_at = EXCLUDED.paid_at,
    created_at = EXCLUDED.created_at
WHERE (
    warehouse.fact_payments.order_id,
    warehouse.fact_payments.payment_status,
    warehouse.fact_payments.amount_vnd,
    warehouse.fact_payments.paid_at,
    warehouse.fact_payments.created_at
) IS DISTINCT FROM (
    EXCLUDED.order_id,
    EXCLUDED.payment_status,
    EXCLUDED.amount_vnd,
    EXCLUDED.paid_at,
    EXCLUDED.created_at
);


-- ============================================================
-- 5. FACT_REVIEWS
-- ============================================================

INSERT INTO warehouse.fact_reviews (
    review_id,
    product_id,
    user_id,
    rating,
    comment,
    created_at
)
SELECT
    review_id,
    product_id,
    user_id,
    rating::NUMERIC,
    comment,
    created_at::TIMESTAMPTZ
FROM raw.fact_reviews
ON CONFLICT (review_id)
DO UPDATE SET
    product_id = EXCLUDED.product_id,
    user_id = EXCLUDED.user_id,
    rating = EXCLUDED.rating,
    comment = EXCLUDED.comment,
    created_at = EXCLUDED.created_at
WHERE (
    warehouse.fact_reviews.product_id,
    warehouse.fact_reviews.user_id,
    warehouse.fact_reviews.rating,
    warehouse.fact_reviews.comment,
    warehouse.fact_reviews.created_at
) IS DISTINCT FROM (
    EXCLUDED.product_id,
    EXCLUDED.user_id,
    EXCLUDED.rating,
    EXCLUDED.comment,
    EXCLUDED.created_at
);


-- ============================================================
-- 6. FACT_PRODUCT_SALES
-- ============================================================

INSERT INTO warehouse.fact_product_sales (
    product_id,
    month,
    year,
    quantity_sold,
    revenue
)
SELECT
    product_id,
    month::INTEGER,
    year::INTEGER,
    quantity_sold::INTEGER,
    revenue::NUMERIC
FROM raw.fact_product_sales
ON CONFLICT (product_id, month, year)
DO UPDATE SET
    quantity_sold = EXCLUDED.quantity_sold,
    revenue = EXCLUDED.revenue
WHERE (
    warehouse.fact_product_sales.quantity_sold,
    warehouse.fact_product_sales.revenue
) IS DISTINCT FROM (
    EXCLUDED.quantity_sold,
    EXCLUDED.revenue
);


-- ============================================================
-- 7. DIM_INVENTORY_STATUS
-- ============================================================

INSERT INTO warehouse.dim_inventory_status (
    product_id,
    product_name,
    variant_id,
    stock,
    is_low_stock,
    created_at
)
SELECT
    product_id,
    product_name,
    variant_id,
    stock::INTEGER,
    CASE
        WHEN LOWER(TRIM(is_low_stock::TEXT))
            IN ('1', 'true', 't', 'yes') THEN TRUE
        WHEN LOWER(TRIM(is_low_stock::TEXT))
            IN ('0', 'false', 'f', 'no') THEN FALSE
        ELSE NULL
    END,
    created_at::TIMESTAMPTZ
FROM raw.dim_inventory_status
ON CONFLICT (product_id, variant_id, created_at)
DO UPDATE SET
    product_name = EXCLUDED.product_name,
    stock = EXCLUDED.stock,
    is_low_stock = EXCLUDED.is_low_stock
WHERE (
    warehouse.dim_inventory_status.product_name,
    warehouse.dim_inventory_status.stock,
    warehouse.dim_inventory_status.is_low_stock
) IS DISTINCT FROM (
    EXCLUDED.product_name,
    EXCLUDED.stock,
    EXCLUDED.is_low_stock
);