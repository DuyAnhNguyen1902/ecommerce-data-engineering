from datetime import datetime, timezone
from pathlib import Path

from config.logging_config import logger
from ingestion.audit import insert_etl_log
from ingestion.database import (
    PostgreSQL,
    count_table_rows,
    run_sql_file,
)


JOB_NAME = "load_warehouse"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

WAREHOUSE_INIT_SQL = (
    PROJECT_ROOT / "sql" / "warehouse_init.sql"
)

WAREHOUSE_INCREMENTAL_SQL = (
    PROJECT_ROOT / "sql" / "warehouse_incremental.sql"
)

WAREHOUSE_TABLES = [
    "dim_products",
    "fact_orders",
    "fact_order_items",
    "fact_payments",
    "fact_reviews",
    "fact_product_sales",
    "dim_inventory_status",
]


def record_failed_audit(
    db,
    start_time,
    end_time,
    error,
):
    try:
        insert_etl_log(
            db=db,
            job_name=JOB_NAME,
            table_name="warehouse_layer",
            start_time=start_time,
            end_time=end_time,
            status="FAILED",
            rows_loaded=0,
            error_message=str(error),
            commit=True,
        )

    except Exception:
        logger.exception(
            "Could not record FAILED Warehouse audit"
        )


def load_warehouse():
    start_time = datetime.now(timezone.utc)
    db = PostgreSQL()

    logger.info("Starting Warehouse load")

    try:
        run_sql_file(
            db=db,
            file_path=WAREHOUSE_INIT_SQL,
            commit=False,
        )

        logger.info(
            "Warehouse tables initialized | file=%s",
            WAREHOUSE_INIT_SQL,
        )

        run_sql_file(
            db=db,
            file_path=WAREHOUSE_INCREMENTAL_SQL,
            commit=False,
        )

        rows_after_load = count_table_rows(
            db=db,
            schema_name="warehouse",
            table_names=WAREHOUSE_TABLES,
        )

        end_time = datetime.now(timezone.utc)

        insert_etl_log(
            db=db,
            job_name=JOB_NAME,
            table_name="warehouse_layer",
            start_time=start_time,
            end_time=end_time,
            status="SUCCESS",
            rows_loaded=rows_after_load,
            error_message=None,
            commit=False,
        )

        db.commit()

        logger.info(
            "Warehouse load completed successfully | "
            "tables=%s | rows_after_load=%s | duration=%s",
            len(WAREHOUSE_TABLES),
            rows_after_load,
            end_time - start_time,
        )

    except Exception as error:
        db.rollback()

        end_time = datetime.now(timezone.utc)

        logger.exception(
            "Warehouse load failed | duration=%s",
            end_time - start_time,
        )

        record_failed_audit(
            db=db,
            start_time=start_time,
            end_time=end_time,
            error=error,
        )

        raise

    finally:
        db.close()
        logger.info("PostgreSQL connection closed")


if __name__ == "__main__":
    load_warehouse()