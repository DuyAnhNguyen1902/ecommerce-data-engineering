from ingestion.database import PostgreSQL


def execute_scalar(db, query):
    """
    Execute a SQL query that returns a single value.
    """
    db.cursor.execute(query)
    return db.cursor.fetchone()[0]


def check_table_not_empty(db, table):
    """
    Check whether a table contains at least one row.
    """
    count = execute_scalar(
        db,
        f"SELECT COUNT(*) FROM {table};"
    )

    if count == 0:
        raise Exception(f"{table} is empty")

    print(f"✓ {table}: {count} rows")


def check_null_order_id(db):
    """
    Check whether warehouse.fact_orders contains NULL order_id values.
    """
    count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM warehouse.fact_orders
        WHERE order_id IS NULL;
        """
    )

    if count > 0:
        raise Exception(
            f"warehouse.fact_orders contains {count} NULL order_id values"
        )

    print("✓ No NULL order_id found")


def check_duplicate_order_id(db):
    """
    Check whether warehouse.fact_orders contains duplicate order_id values.
    """
    count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM (
            SELECT order_id
            FROM warehouse.fact_orders
            GROUP BY order_id
            HAVING COUNT(*) > 1
        ) AS duplicate_orders;
        """
    )

    if count > 0:
        raise Exception(
            f"warehouse.fact_orders contains {count} duplicate order_id values"
        )

    print("✓ No duplicate order_id found")


def check_order_item_integrity(db):
    """
    Check whether any order item references an order that does not exist.
    """
    count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM warehouse.fact_order_items AS i
        LEFT JOIN warehouse.fact_orders AS o
            ON i.order_id = o.order_id
        WHERE o.order_id IS NULL;
        """
    )

    if count > 0:
        raise Exception(
            f"warehouse.fact_order_items contains {count} orphan records"
        )

    print("✓ No orphan order_items found")


def check_negative_order_values(db):
    """
    Check whether order values contain invalid negative numbers.
    """
    count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM warehouse.fact_orders
        WHERE final_total < 0
           OR discount_value < 0;
        """
    )

    if count > 0:
        raise Exception(
            f"warehouse.fact_orders contains {count} invalid negative values"
        )

    print("✓ No negative order values found")


def check_invalid_order_item_values(db):
    """
    Check whether order items contain invalid quantity or price values.
    """
    count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM warehouse.fact_order_items
        WHERE quantity <= 0
           OR price < 0
           OR line_total < 0;
        """
    )

    if count > 0:
        raise Exception(
            f"warehouse.fact_order_items contains {count} invalid values"
        )

    print("✓ Order item quantities and prices are valid")


def check_invalid_review_rating(db):
    """
    Check whether review ratings are outside the valid range from 1 to 5.
    """
    count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM warehouse.fact_reviews
        WHERE rating IS NOT NULL
          AND (rating < 1 OR rating > 5);
        """
    )

    if count > 0:
        raise Exception(
            f"warehouse.fact_reviews contains {count} invalid rating values"
        )

    print("✓ Review ratings are within the valid range")


def check_raw_warehouse_order_count(db):
    """
    Compare the number of orders between Raw and Warehouse layers.
    """
    raw_count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM raw.fact_orders;
        """
    )

    warehouse_count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM warehouse.fact_orders;
        """
    )

    if warehouse_count < raw_count:
        raise Exception(
            "Warehouse order count is lower than Raw order count: "
            f"raw={raw_count}, warehouse={warehouse_count}"
        )

    print(
        "✓ Raw and Warehouse order counts are valid "
        f"(raw={raw_count}, warehouse={warehouse_count})"
    )


def run_quality_check():
    """
    Run all data quality checks.
    """
    db = PostgreSQL()

    print("=" * 60)
    print("Running Data Quality Checks...")
    print("=" * 60)

    try:
        critical_tables = [
            "raw.fact_orders",
            "raw.fact_order_items",
            "warehouse.fact_orders",
            "warehouse.fact_order_items",
            "warehouse.fact_payments",
            "warehouse.fact_reviews",
            "mart.revenue_by_month",
            "mart.top_products",
            "mart.payment_funnel",
        ]

        for table in critical_tables:
            check_table_not_empty(db, table)

        check_null_order_id(db)
        check_duplicate_order_id(db)
        check_order_item_integrity(db)
        check_negative_order_values(db)
        check_invalid_order_item_values(db)
        check_invalid_review_rating(db)
        check_raw_warehouse_order_count(db)

        print("=" * 60)
        print("All Data Quality Checks Passed")
        print("=" * 60)

    except Exception as error:
        print("=" * 60)
        print(f"Data Quality Check Failed: {error}")
        print("=" * 60)
        raise

    finally:
        db.close()


if __name__ == "__main__":
    run_quality_check()