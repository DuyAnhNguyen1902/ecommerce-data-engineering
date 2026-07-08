from datetime import datetime

from ingestion.excel_reader import ExcelReader
from ingestion.database import PostgreSQL
from ingestion.table_creator import create_raw_table
from ingestion.loader import truncate_raw_table, insert_dataframe_to_raw
from ingestion.audit import insert_etl_log
from config.logging_config import logger


def load_raw():
    reader = ExcelReader()
    tables = reader.read_latest_file()

    db = PostgreSQL()

    try:
        for table_name, df in tables.items():
            start_time = datetime.now()
            rows_loaded = len(df)

            try:
                logger.info(f"Start loading raw.{table_name}")
                print(f"Loading raw.{table_name}")

                create_raw_table(db, df, table_name)
                truncate_raw_table(db, table_name)
                insert_dataframe_to_raw(db, df, table_name)

                end_time = datetime.now()

                insert_etl_log(
                    db=db,
                    job_name="load_raw",
                    table_name=table_name,
                    start_time=start_time,
                    end_time=end_time,
                    status="SUCCESS",
                    rows_loaded=rows_loaded
                )

                logger.info(f"Loaded raw.{table_name} successfully | rows={rows_loaded}")

            except Exception as e:
                end_time = datetime.now()

                insert_etl_log(
                    db=db,
                    job_name="load_raw",
                    table_name=table_name,
                    start_time=start_time,
                    end_time=end_time,
                    status="FAILED",
                    rows_loaded=0,
                    error_message=str(e)
                )

                logger.error(f"Failed loading raw.{table_name}: {e}")
                raise

        print("✅ RAW LOAD DONE")
        logger.info("RAW LOAD DONE")

    finally:
        db.close()


if __name__ == "__main__":
    load_raw()