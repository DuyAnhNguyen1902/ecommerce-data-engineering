from datetime import datetime, timezone
from pathlib import Path

from config.logging_config import logger
from ingestion.audit import insert_etl_log
from ingestion.database import (
    PostgreSQL,
    count_table_rows,
    run_sql_file,
)


JOB_NAME = "load_mart"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MART_INIT_SQL = PROJECT_ROOT / "sql" / "mart_init.sql"
MART_REFRESH_SQL = PROJECT_ROOT / "sql" / "mart_refresh.sql"

MART_TABLES = [
    "revenue_by_month",
    "top_products",
    "payment_funnel",
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
            table_name="mart_layer",
            start_time=start_time,
            end_time=end_time,
            status="FAILED",
            rows_loaded=0,
            error_message=str(error),
            commit=True,
        )

    except Exception:
        logger.exception(
            "Could not record FAILED Mart audit"
        )


def load_mart():
    start_time = datetime.now(timezone.utc)
    db = PostgreSQL()

    logger.info("Starting Mart refresh")

    try:
        run_sql_file(
            db=db,
            file_path=MART_INIT_SQL,
            commit=False,
        )

        logger.info(
            "Mart tables initialized | file=%s",
            MART_INIT_SQL,
        )

        run_sql_file(
            db=db,
            file_path=MART_REFRESH_SQL,
            commit=False,
        )

        rows_after_load = count_table_rows(
            db=db,
            schema_name="mart",
            table_names=MART_TABLES,
        )

        end_time = datetime.now(timezone.utc)

        insert_etl_log(
            db=db,
            job_name=JOB_NAME,
            table_name="mart_layer",
            start_time=start_time,
            end_time=end_time,
            status="SUCCESS",
            rows_loaded=rows_after_load,
            error_message=None,
            commit=False,
        )

        db.commit()

        logger.info(
            "Mart refresh completed successfully | "
            "tables=%s | rows_after_load=%s | duration=%s",
            len(MART_TABLES),
            rows_after_load,
            end_time - start_time,
        )

    except Exception as error:
        db.rollback()

        end_time = datetime.now(timezone.utc)

        logger.exception(
            "Mart refresh failed | duration=%s",
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
    load_mart()