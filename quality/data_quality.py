from datetime import datetime, timezone

from psycopg2 import sql

from config.logging_config import logger
from ingestion.audit import insert_etl_log
from ingestion.database import PostgreSQL


JOB_NAME = "data_quality_check"


def execute_scalar(db, query, params=None):
    """
    Execute a SQL query that returns one scalar value.
    """
    db.cursor.execute(query, params)
    return db.cursor.fetchone()[0]


def check_table_not_empty(db, table_name):
    """
    Check whether a critical table contains at least one row.
    """
    schema_name, relation_name = table_name.split(".", maxsplit=1)

    query = sql.SQL(
        "SELECT COUNT(*) FROM {}.{};"
    ).format(
        sql.Identifier(schema_name),
        sql.Identifier(relation_name),
    )

    row_count = execute_scalar(db, query)

    if row_count == 0:
        raise ValueError(f"{table_name} is empty")

    logger.info(
        "Data quality passed | table=%s | rows=%s",
        table_name,
        row_count,
    )


def check_null_order_id(db):
    """
    Check NULL order IDs in Warehouse.
    """
    invalid_count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM warehouse.fact_orders
        WHERE order_id IS NULL;
        """,
    )

    if invalid_count > 0:
        raise ValueError(
            "warehouse.fact_orders contains "
            f"{invalid_count} NULL order_id values"
        )

    logger.info("Data quality passed | no NULL order_id")


def check_duplicate_order_id(db):
    """
    Check duplicate order IDs in Warehouse.
    """
    duplicate_count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM (
            SELECT order_id
            FROM warehouse.fact_orders
            GROUP BY order_id
            HAVING COUNT(*) > 1
        ) AS duplicate_orders;
        """,
    )

    if duplicate_count > 0:
        raise ValueError(
            "warehouse.fact_orders contains "
            f"{duplicate_count} duplicate order_id values"
        )

    logger.info("Data quality passed | no duplicate order_id")


def check_order_item_integrity(db):
    """
    Check order items that reference missing orders.
    """
    orphan_count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM warehouse.fact_order_items AS item
        LEFT JOIN warehouse.fact_orders AS order_data
            ON item.order_id = order_data.order_id
        WHERE order_data.order_id IS NULL;
        """,
    )

    if orphan_count > 0:
        raise ValueError(
            "warehouse.fact_order_items contains "
            f"{orphan_count} orphan records"
        )

    logger.info("Data quality passed | no orphan order items")


def check_product_integrity(db):
    """
    Check order items that reference missing products.
    """
    orphan_count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM warehouse.fact_order_items AS item
        LEFT JOIN warehouse.dim_products AS product
            ON item.product_id = product.product_id
        WHERE product.product_id IS NULL;
        """,
    )

    if orphan_count > 0:
        raise ValueError(
            "warehouse.fact_order_items contains "
            f"{orphan_count} unknown product references"
        )

    logger.info("Data quality passed | no orphan product references")


def check_payment_integrity(db):
    """
    Check payments that reference missing orders.
    """
    orphan_count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM warehouse.fact_payments AS payment
        LEFT JOIN warehouse.fact_orders AS order_data
            ON payment.order_id = order_data.order_id
        WHERE order_data.order_id IS NULL;
        """,
    )

    if orphan_count > 0:
        raise ValueError(
            "warehouse.fact_payments contains "
            f"{orphan_count} orphan records"
        )

    logger.info("Data quality passed | no orphan payments")


def check_negative_order_values(db):
    """
    Check invalid negative order values.
    """
    invalid_count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM warehouse.fact_orders
        WHERE final_total < 0
           OR discount_value < 0;
        """,
    )

    if invalid_count > 0:
        raise ValueError(
            "warehouse.fact_orders contains "
            f"{invalid_count} negative values"
        )

    logger.info("Data quality passed | order values are valid")


def check_invalid_order_item_values(db):
    """
    Check invalid quantity, price, or line total.
    """
    invalid_count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM warehouse.fact_order_items
        WHERE quantity <= 0
           OR price < 0
           OR line_total < 0;
        """,
    )

    if invalid_count > 0:
        raise ValueError(
            "warehouse.fact_order_items contains "
            f"{invalid_count} invalid values"
        )

    logger.info("Data quality passed | order item values are valid")


def check_invalid_payment_values(db):
    """
    Check invalid payment amounts.
    """
    invalid_count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM warehouse.fact_payments
        WHERE amount_vnd < 0;
        """,
    )

    if invalid_count > 0:
        raise ValueError(
            "warehouse.fact_payments contains "
            f"{invalid_count} negative amounts"
        )

    logger.info("Data quality passed | payment amounts are valid")


def check_invalid_review_rating(db):
    """
    Check whether ratings are outside the range 1 to 5.
    """
    invalid_count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM warehouse.fact_reviews
        WHERE rating IS NOT NULL
          AND (rating < 1 OR rating > 5);
        """,
    )

    if invalid_count > 0:
        raise ValueError(
            "warehouse.fact_reviews contains "
            f"{invalid_count} invalid ratings"
        )

    logger.info("Data quality passed | review ratings are valid")


def check_raw_orders_loaded_to_warehouse(db):
    """
    Check whether every non-NULL Raw order exists in Warehouse.

    Warehouse may contain historical records, so equality between total
    Raw and Warehouse row counts is not required.
    """
    missing_count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM (
            SELECT DISTINCT order_id
            FROM raw.fact_orders
            WHERE order_id IS NOT NULL
        ) AS raw_order
        LEFT JOIN warehouse.fact_orders AS warehouse_order
            ON raw_order.order_id = warehouse_order.order_id
        WHERE warehouse_order.order_id IS NULL;
        """,
    )

    if missing_count > 0:
        raise ValueError(
            f"{missing_count} Raw orders are missing from Warehouse"
        )

    logger.info(
        "Data quality passed | all Raw orders exist in Warehouse"
    )


def check_mart_month_values(db):
    """
    Check valid year and month values in the monthly Mart table.
    """
    invalid_count = execute_scalar(
        db,
        """
        SELECT COUNT(*)
        FROM mart.revenue_by_month
        WHERE year IS NULL
           OR month IS NULL
           OR month NOT BETWEEN 1 AND 12;
        """,
    )

    if invalid_count > 0:
        raise ValueError(
            "mart.revenue_by_month contains "
            f"{invalid_count} invalid year/month values"
        )

    logger.info("Data quality passed | Mart month values are valid")


def check_revenue_mart_reconciliation(db):
    """
    Reconcile completed-order monthly KPIs between Warehouse and Mart.
    """
    mismatch_count = execute_scalar(
        db,
        """
        WITH expected AS (
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
            WHERE created_at IS NOT NULL
              AND LOWER(TRIM(status)) = 'completed'
            GROUP BY 1, 2
        )
        SELECT COUNT(*)
        FROM expected AS expected_data
        FULL OUTER JOIN mart.revenue_by_month AS mart_data
            ON expected_data.year = mart_data.year
           AND expected_data.month = mart_data.month
        WHERE expected_data.year IS NULL
           OR mart_data.year IS NULL
           OR expected_data.total_orders
                IS DISTINCT FROM mart_data.total_orders
           OR expected_data.total_revenue
                IS DISTINCT FROM mart_data.total_revenue
           OR expected_data.total_discount
                IS DISTINCT FROM mart_data.total_discount
           OR expected_data.unique_customers
                IS DISTINCT FROM mart_data.unique_customers;
        """,
    )

    if mismatch_count > 0:
        raise ValueError(
            "mart.revenue_by_month contains "
            f"{mismatch_count} rows that do not match Warehouse"
        )

    logger.info(
        "Data quality passed | revenue Mart matches Warehouse"
    )


def check_top_products_reconciliation(db):
    """
    Reconcile completed-order product KPIs.
    """
    mismatch_count = execute_scalar(
        db,
        """
        WITH expected AS (
            SELECT
                item.product_id,
                COALESCE(product.product_name, 'Unknown Product')
                    AS product_name,
                COALESCE(product.category, 'Unknown Category')
                    AS category,
                COALESCE(SUM(item.quantity), 0)
                    AS total_quantity_sold,
                COALESCE(SUM(item.line_total), 0)::NUMERIC(20, 2)
                    AS total_revenue,
                COUNT(DISTINCT item.order_id)
                    AS order_count
            FROM warehouse.fact_order_items AS item
            INNER JOIN warehouse.fact_orders AS order_data
                ON item.order_id = order_data.order_id
            LEFT JOIN warehouse.dim_products AS product
                ON item.product_id = product.product_id
            WHERE LOWER(TRIM(order_data.status)) = 'completed'
            GROUP BY
                item.product_id,
                product.product_name,
                product.category
        )
        SELECT COUNT(*)
        FROM expected AS expected_data
        FULL OUTER JOIN mart.top_products AS mart_data
            ON expected_data.product_id = mart_data.product_id
        WHERE expected_data.product_id IS NULL
           OR mart_data.product_id IS NULL
           OR expected_data.product_name
                IS DISTINCT FROM mart_data.product_name
           OR expected_data.category
                IS DISTINCT FROM mart_data.category
           OR expected_data.total_quantity_sold
                IS DISTINCT FROM mart_data.total_quantity_sold
           OR expected_data.total_revenue
                IS DISTINCT FROM mart_data.total_revenue
           OR expected_data.order_count
                IS DISTINCT FROM mart_data.order_count;
        """,
    )

    if mismatch_count > 0:
        raise ValueError(
            "mart.top_products contains "
            f"{mismatch_count} rows that do not match Warehouse"
        )

    logger.info(
        "Data quality passed | top-products Mart matches Warehouse"
    )


def check_payment_funnel_reconciliation(db):
    """
    Reconcile payment KPIs between Warehouse and Mart.
    """
    mismatch_count = execute_scalar(
        db,
        """
        WITH expected AS (
            SELECT
                COALESCE(
                    NULLIF(UPPER(TRIM(payment_status)), ''),
                    'UNKNOWN'
                ) AS payment_status,
                COUNT(*) AS payment_count,
                COALESCE(SUM(amount_vnd), 0)::NUMERIC(20, 2)
                    AS total_amount
            FROM warehouse.fact_payments
            GROUP BY 1
        )
        SELECT COUNT(*)
        FROM expected AS expected_data
        FULL OUTER JOIN mart.payment_funnel AS mart_data
            ON expected_data.payment_status = mart_data.payment_status
        WHERE expected_data.payment_status IS NULL
           OR mart_data.payment_status IS NULL
           OR expected_data.payment_count
                IS DISTINCT FROM mart_data.payment_count
           OR expected_data.total_amount
                IS DISTINCT FROM mart_data.total_amount;
        """,
    )

    if mismatch_count > 0:
        raise ValueError(
            "mart.payment_funnel contains "
            f"{mismatch_count} rows that do not match Warehouse"
        )

    logger.info(
        "Data quality passed | payment Mart matches Warehouse"
    )


def record_failed_audit(db, start_time, end_time, error):
    """
    Record a failed Data Quality run in a new transaction.
    """
    try:
        insert_etl_log(
            db=db,
            job_name=JOB_NAME,
            table_name="pipeline_data",
            start_time=start_time,
            end_time=end_time,
            status="FAILED",
            rows_loaded=0,
            error_message=str(error),
            commit=True,
        )

    except Exception:
        logger.exception(
            "Could not record FAILED Data Quality audit"
        )


def run_quality_check():
    """
    Run all Data Quality checks and record the result.
    """
    start_time = datetime.now(timezone.utc)
    db = PostgreSQL()
    passed_checks = 0

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

    quality_checks = [
        check_null_order_id,
        check_duplicate_order_id,
        check_order_item_integrity,
        check_product_integrity,
        check_payment_integrity,
        check_negative_order_values,
        check_invalid_order_item_values,
        check_invalid_payment_values,
        check_invalid_review_rating,
        check_raw_orders_loaded_to_warehouse,
        check_mart_month_values,
        check_revenue_mart_reconciliation,
        check_top_products_reconciliation,
        check_payment_funnel_reconciliation,
    ]

    logger.info("Starting Data Quality checks")

    try:
        for table_name in critical_tables:
            check_table_not_empty(db, table_name)
            passed_checks += 1

        for quality_check in quality_checks:
            quality_check(db)
            passed_checks += 1

        end_time = datetime.now(timezone.utc)

        insert_etl_log(
            db=db,
            job_name=JOB_NAME,
            table_name="pipeline_data",
            start_time=start_time,
            end_time=end_time,
            status="SUCCESS",
            rows_loaded=passed_checks,
            error_message=None,
            commit=True,
        )

        logger.info(
            "All Data Quality checks passed | "
            "checks=%s | duration=%s",
            passed_checks,
            end_time - start_time,
        )

    except Exception as error:
        db.rollback()

        end_time = datetime.now(timezone.utc)

        logger.exception(
            "Data Quality check failed | "
            "passed_checks=%s | duration=%s",
            passed_checks,
            end_time - start_time,
        )

        record_failed_audit(
            db=db,
            start_time=start_time,
            end_time=end_time,
            error=error,
        )

        # Quan trọng: truyền lỗi cho Airflow để task chuyển sang FAILED.
        raise

    finally:
        db.close()
        logger.info("PostgreSQL connection closed")


if __name__ == "__main__":
    run_quality_check()