from ingestion.database import PostgreSQL


def check_table(table):
    db = PostgreSQL()

    db.cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = db.cursor.fetchone()[0]

    db.close()

    if count == 0:
        raise Exception(f"{table} is empty")

    print(f"✓ {table}: {count} rows")


def run_quality_check():

    print("Running Data Quality Check...")

    tables = [
        "raw.fact_orders",
        "warehouse.fact_orders",
        "mart.revenue_by_month"
    ]

    for table in tables:
        check_table(table)

    print("All quality checks passed.")


if __name__ == "__main__":
    run_quality_check()