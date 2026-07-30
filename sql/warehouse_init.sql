CREATE SCHEMA IF NOT EXISTS warehouse;


CREATE TABLE IF NOT EXISTS warehouse.dim_products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    price NUMERIC(18, 2)
);


CREATE TABLE IF NOT EXISTS warehouse.fact_orders (
    order_id TEXT PRIMARY KEY,
    user_id TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    final_total NUMERIC(18, 2),
    discount_value NUMERIC(18, 2),
    status TEXT,
    payment_method TEXT
);


CREATE TABLE IF NOT EXISTS warehouse.fact_order_items (
    order_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    variant_id TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price NUMERIC(18, 2),
    line_total NUMERIC(18, 2),

    PRIMARY KEY (
        order_id,
        product_id,
        variant_id
    )
);


CREATE TABLE IF NOT EXISTS warehouse.fact_payments (
    payment_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    payment_status TEXT,
    amount_vnd NUMERIC(18, 2),
    paid_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ
);


CREATE TABLE IF NOT EXISTS warehouse.fact_reviews (
    review_id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL,
    user_id TEXT,
    rating NUMERIC(2, 1),
    comment TEXT,
    created_at TIMESTAMPTZ
);


CREATE TABLE IF NOT EXISTS warehouse.fact_product_sales (
    product_id TEXT NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    quantity_sold INTEGER,
    revenue NUMERIC(18, 2),

    PRIMARY KEY (
        product_id,
        month,
        year
    ),

    CHECK (month BETWEEN 1 AND 12),
    CHECK (quantity_sold >= 0)
);


CREATE TABLE IF NOT EXISTS warehouse.dim_inventory_status (
    product_id TEXT NOT NULL,
    product_name TEXT,
    variant_id TEXT NOT NULL,
    stock INTEGER,
    is_low_stock BOOLEAN,
    created_at TIMESTAMPTZ NOT NULL,

    PRIMARY KEY (
        product_id,
        variant_id,
        created_at
    ),

    CHECK (stock >= 0)
);


CREATE INDEX IF NOT EXISTS idx_fact_orders_created_at
    ON warehouse.fact_orders (created_at);

CREATE INDEX IF NOT EXISTS idx_fact_orders_user_id
    ON warehouse.fact_orders (user_id);

CREATE INDEX IF NOT EXISTS idx_fact_orders_status
    ON warehouse.fact_orders (status);

CREATE INDEX IF NOT EXISTS idx_fact_order_items_product_id
    ON warehouse.fact_order_items (product_id);

CREATE INDEX IF NOT EXISTS idx_fact_payments_order_id
    ON warehouse.fact_payments (order_id);

CREATE INDEX IF NOT EXISTS idx_fact_reviews_product_id
    ON warehouse.fact_reviews (product_id);

CREATE INDEX IF NOT EXISTS idx_inventory_product_id
    ON warehouse.dim_inventory_status (product_id);