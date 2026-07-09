INSERT INTO warehouse.dim_products (
    product_id, product_name, category, price
)
SELECT
    "Product_id",
    "Product_name",
    "Category",
    "Price"::NUMERIC
FROM raw.dim_products
ON CONFLICT (product_id)
DO UPDATE SET
    product_name = EXCLUDED.product_name,
    category = EXCLUDED.category,
    price = EXCLUDED.price;


INSERT INTO warehouse.fact_orders (
    order_id, user_id, created_at, final_total,
    discount_value, status, payment_method
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
    payment_method = EXCLUDED.payment_method;


INSERT INTO warehouse.fact_order_items (
    order_id, product_id, variant_id, quantity, price, line_total
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
    line_total = EXCLUDED.line_total;


INSERT INTO warehouse.fact_payments (
    payment_id, order_id, payment_status, amount_vnd, paid_at, created_at
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
    created_at = EXCLUDED.created_at;


INSERT INTO warehouse.fact_reviews (
    review_id, product_id, user_id, rating, comment, created_at
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
    created_at = EXCLUDED.created_at;


INSERT INTO warehouse.fact_product_sales (
    product_id, month, year, quantity_sold, revenue
)
SELECT
    "Product_id",
    "Month"::INTEGER,
    "Year"::INTEGER,
    "Quantity_sold"::INTEGER,
    "Revenue"::NUMERIC
FROM raw.fact_product_sales
ON CONFLICT (product_id, month, year)
DO UPDATE SET
    quantity_sold = EXCLUDED.quantity_sold,
    revenue = EXCLUDED.revenue;


INSERT INTO warehouse.dim_inventory_status (
    product_id, product_name, variant_id, stock, is_low_stock, created_at
)
SELECT
    product_id,
    product_name,
    variant_id,
    stock::INTEGER,
    CASE
        WHEN is_low_stock = 1 THEN TRUE
        ELSE FALSE
    END,
    created_at::TIMESTAMPTZ
FROM raw.dim_inventory_status
ON CONFLICT (product_id, variant_id, created_at)
DO UPDATE SET
    product_name = EXCLUDED.product_name,
    stock = EXCLUDED.stock,
    is_low_stock = EXCLUDED.is_low_stock;