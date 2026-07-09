from warehouse.load_warehouse import run_sql_file


def load_mart():
    print("Running mart init SQL...")
    run_sql_file("sql/mart_init.sql")

    print("Running mart refresh SQL...")
    run_sql_file("sql/mart_refresh.sql")

    print("✅ Mart refresh done")


if __name__ == "__main__":
    load_mart()