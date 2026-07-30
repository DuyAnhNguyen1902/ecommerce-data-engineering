from datetime import datetime

from config.logging_config import logger
from ingestion.audit import insert_etl_log
from ingestion.database import PostgreSQL
from ingestion.excel_reader import ExcelReader
from ingestion.loader import (
    insert_dataframe_to_raw,
    truncate_raw_table,
)
from ingestion.table_creator import create_raw_table


JOB_NAME = "load_raw"


def record_failed_audit(
    db,
    table_name,
    start_time,
    end_time,
    error,
):
    """
    Record a FAILED audit after the failed data transaction
    has already been rolled back.

    Audit failures are logged separately so they do not hide
    the original ETL exception.
    """
    try:
        insert_etl_log(
            db=db,
            job_name=JOB_NAME,
            table_name=table_name,
            start_time=start_time,
            end_time=end_time,
            status="FAILED",
            rows_loaded=0,
            error_message=str(error),
            commit=True,
        )

    except Exception:
        logger.exception(
            "Could not record FAILED audit | "
            "job=%s | table=%s",
            JOB_NAME,
            table_name,
        )


def load_raw():
    logger.info("Starting Raw load")

    reader = ExcelReader()
    tables = reader.read_latest_file()

    db = PostgreSQL()

    try:
        for table_name, dataframe in tables.items():
            start_time = datetime.now()

            logger.info(
                "Loading Raw table | table=raw.%s | source_rows=%s",
                table_name,
                len(dataframe),
            )

            try:
                # These operations belong to the same transaction.
                create_raw_table(
                    db=db,
                    dataframe=dataframe,
                    table_name=table_name,
                )

                truncate_raw_table(
                    db=db,
                    table_name=table_name,
                )

                rows_loaded = insert_dataframe_to_raw(
                    db=db,
                    dataframe=dataframe,
                    table_name=table_name,
                )

                end_time = datetime.now()

                # commit=False keeps the SUCCESS audit in the
                # same transaction as TRUNCATE and INSERT.
                insert_etl_log(
                    db=db,
                    job_name=JOB_NAME,
                    table_name=table_name,
                    start_time=start_time,
                    end_time=end_time,
                    status="SUCCESS",
                    rows_loaded=rows_loaded,
                    error_message=None,
                    commit=False,
                )

                db.commit()

                logger.info(
                    "Raw table loaded successfully | "
                    "table=raw.%s | rows=%s | duration=%s",
                    table_name,
                    rows_loaded,
                    end_time - start_time,
                )

            except Exception as error:
                # Roll back CREATE/TRUNCATE/INSERT and any
                # uncommitted SUCCESS audit.
                db.rollback()

                end_time = datetime.now()

                logger.exception(
                    "Raw table load failed | "
                    "table=raw.%s | duration=%s",
                    table_name,
                    end_time - start_time,
                )

                record_failed_audit(
                    db=db,
                    table_name=table_name,
                    start_time=start_time,
                    end_time=end_time,
                    error=error,
                )

                # Make Airflow mark the task as FAILED.
                raise

        logger.info(
            "Raw load completed successfully | tables=%s",
            len(tables),
        )

    finally:
        db.close()
        logger.info("PostgreSQL connection closed")


if __name__ == "__main__":
    load_raw()