import psycopg2
from psycopg2 import sql

from config.settings import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


class PostgreSQL:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )

        self.cursor = self.conn.cursor()

    def execute(
        self,
        query,
        params=None,
        commit=True,
    ):
        try:
            self.cursor.execute(query, params)

            if commit:
                self.conn.commit()

        except Exception:
            self.conn.rollback()
            raise

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        if self.cursor and not self.cursor.closed:
            self.cursor.close()

        if self.conn and not self.conn.closed:
            self.conn.close()


def run_sql_file(
    db,
    file_path,
    commit=False,
):
    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as sql_file:
        statement = sql_file.read()

    db.execute(
        statement,
        commit=commit,
    )


def count_table_rows(
    db,
    schema_name,
    table_names,
):
    total_rows = 0

    for table_name in table_names:
        query = sql.SQL(
            "SELECT COUNT(*) FROM {}.{}"
        ).format(
            sql.Identifier(schema_name),
            sql.Identifier(table_name),
        )

        db.cursor.execute(query)
        total_rows += db.cursor.fetchone()[0]

    return total_rows