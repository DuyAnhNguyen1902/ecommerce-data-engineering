from ingestion.database import PostgreSQL
from config.logging_config import logger


def run_sql_file(file_path):
    db = PostgreSQL()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            sql = file.read()

        db.execute(sql)
        logger.info("Executed SQL file: %s", file_path)

    finally:
        db.close()


def load_warehouse():
    print("Running warehouse init SQL...")
    run_sql_file("sql/warehouse_init.sql")

    print("Running warehouse incremental SQL...")
    run_sql_file("sql/warehouse_incremental.sql")

    print("✅ Warehouse incremental load done")


if __name__ == "__main__":
    load_warehouse()