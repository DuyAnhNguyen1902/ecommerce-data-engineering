from psycopg2 import sql

from ingestion.database import PostgreSQL


class QualityCheckError(RuntimeError):
    """Raised when a data quality rule finds invalid records."""


TABLES_TO_CHECK = (
    "raw.fact_orders",
    "raw.fact_order_items",
    "warehouse.dim_products",
    "warehouse.fact_orders",
    "warehouse.fact_order_items",
    "warehouse.fact_payments",
    "warehouse.fact_reviews",
    "warehouse.fact_product_sales",
    "warehouse.dim_inventory_status",
    "mart.revenue_by_month",
    "mart.top_products",
    "mart.payment_funnel",
)


QUALITY_RULES = (
    (
        "warehouse fact_orders has no NULL order_id",
        "SELECT COUNT(*) FROM warehouse.fact_orders WHERE order_id IS NULL",
    ),
    (
        "warehouse fact_order_items has no NULL business key",
        """
        SELECT COUNT(*)
        FROM warehouse.fact_order_items
        WHERE order_id IS NULL OR product_id IS NULL OR variant_id IS NULL
        """,
    ),
    (
        "warehouse fact_payments has no NULL payment_id",
        "SELECT COUNT(*) FROM warehouse.fact_payments WHERE payment_id IS NULL",
    ),
    (
        "warehouse fact_reviews has no NULL review_id",
        "SELECT COUNT(*) FROM warehouse.fact_reviews WHERE review_id IS NULL",
    ),
    (
        "warehouse dim_products has no duplicate product_id",
        """
        SELECT COUNT(*)
        FROM (
            SELECT product_id
            FROM warehouse.dim_products
            GROUP BY product_id
            HAVING COUNT(*) > 1
        ) AS duplicates
        """,
    ),
    (
        "warehouse fact_orders has no duplicate order_id",
        """
        SELECT COUNT(*)
        FROM (
            SELECT order_id
            FROM warehouse.fact_orders
            GROUP BY order_id
            HAVING COUNT(*) > 1
        ) AS duplicates
        """,
    ),
    (
        "warehouse fact_order_items has no duplicate business key",
        """
        SELECT COUNT(*)
        FROM (
            SELECT order_id, product_id, variant_id
            FROM warehouse.fact_order_items
            GROUP BY order_id, product_id, variant_id
            HAVING COUNT(*) > 1
        ) AS duplicates
        """,
    ),
    (
        "warehouse fact_order_items has no orphan orders",
        """
        SELECT COUNT(*)
        FROM warehouse.fact_order_items AS item
        LEFT JOIN warehouse.fact_orders AS orders
            ON item.order_id = orders.order_id
        WHERE orders.order_id IS NULL
        """,
    ),
    (
        "warehouse orders has no negative monetary values",
        """
        SELECT COUNT(*)
        FROM warehouse.fact_orders
        WHERE final_total < 0 OR discount_value < 0
        """,
    ),
    (
        "warehouse order items has no negative values",
        """
        SELECT COUNT(*)
        FROM warehouse.fact_order_items
        WHERE quantity < 0 OR price < 0 OR line_total < 0
        """,
    ),
    (
        "warehouse payments has no negative amount",
        "SELECT COUNT(*) FROM warehouse.fact_payments WHERE amount_vnd < 0",
    ),
    (
        "warehouse product sales has no negative values",
        """
        SELECT COUNT(*)
        FROM warehouse.fact_product_sales
        WHERE quantity_sold < 0 OR revenue < 0
        """,
    ),
    (
        "warehouse product and inventory values are non-negative",
        """
        SELECT
            (SELECT COUNT(*) FROM warehouse.dim_products WHERE price < 0)
            +
            (SELECT COUNT(*) FROM warehouse.dim_inventory_status WHERE stock < 0)
        """,
    ),
    (
        "warehouse review ratings are between 1 and 5",
        """
        SELECT COUNT(*)
        FROM warehouse.fact_reviews
        WHERE rating IS NOT NULL AND rating NOT BETWEEN 1 AND 5
        """,
    ),
    (
        "mart monthly revenue matches warehouse monthly revenue",
        """
        WITH warehouse_revenue AS (
            SELECT
                EXTRACT(YEAR FROM created_at)::INTEGER AS year,
                EXTRACT(MONTH FROM created_at)::INTEGER AS month,
                SUM(final_total) AS total_revenue
            FROM warehouse.fact_orders
            GROUP BY 1, 2
        )
        SELECT COUNT(*)
        FROM warehouse_revenue AS warehouse
        FULL OUTER JOIN mart.revenue_by_month AS mart
            ON mart.year = warehouse.year
            AND mart.month = warehouse.month
        WHERE warehouse.year IS NULL
            OR mart.year IS NULL
            OR ABS(COALESCE(warehouse.total_revenue, 0)
                - COALESCE(mart.total_revenue, 0)) > 0.01
        """,
    ),
)


def relation_identifier(relation):
    """Return a safely quoted schema-qualified PostgreSQL identifier."""
    parts = relation.split(".")
    if len(parts) != 2 or not all(parts):
        raise ValueError(f"Expected relation in schema.table format: {relation!r}")
    return sql.Identifier(*parts)


def fetch_count(cursor, query):
    cursor.execute(query)
    return cursor.fetchone()[0]


def check_table_not_empty(cursor, relation):
    query = sql.SQL("SELECT COUNT(*) FROM {}").format(
        relation_identifier(relation)
    )
    count = fetch_count(cursor, query)
    if count == 0:
        raise QualityCheckError(f"{relation} is empty")
    print(f"[PASS] {relation}: {count} rows")


def check_zero_invalid_rows(cursor, description, query):
    invalid_count = fetch_count(cursor, query)
    if invalid_count != 0:
        raise QualityCheckError(
            f"{description}: found {invalid_count} invalid row(s)"
        )
    print(f"[PASS] {description}")


def run_quality_check():
    print("Running data quality checks...")
    db = PostgreSQL()

    try:
        for relation in TABLES_TO_CHECK:
            check_table_not_empty(db.cursor, relation)

        for description, query in QUALITY_RULES:
            check_zero_invalid_rows(db.cursor, description, query)
    finally:
        db.close()

    print("All data quality checks passed.")


if __name__ == "__main__":
    run_quality_check()
