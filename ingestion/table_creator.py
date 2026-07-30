from psycopg2 import sql

from ingestion.raw_schema import (
    RAW_TABLE_SCHEMAS,
    SchemaValidationError,
)


POSTGRES_TYPE_NAMES = {
    "TEXT": "text",
    "NUMERIC": "numeric",
    "INTEGER": "integer",
    "TIMESTAMPTZ": "timestamp with time zone",
}


def create_raw_table(db, dataframe, table_name):
    if table_name not in RAW_TABLE_SCHEMAS:
        raise SchemaValidationError(
            f"No Raw schema contract exists for {table_name!r}."
        )

    expected_columns = list(
        RAW_TABLE_SCHEMAS[table_name]
    )

    if list(dataframe.columns) != expected_columns:
        raise SchemaValidationError(
            f"DataFrame columns for raw.{table_name} "
            "do not match the schema contract."
        )

    column_definitions = [
        sql.SQL("{} {}").format(
            sql.Identifier(column_name),
            sql.SQL(postgres_type),
        )
        for column_name, postgres_type
        in RAW_TABLE_SCHEMAS[table_name].items()
    ]

    create_query = sql.SQL(
        "CREATE TABLE IF NOT EXISTS {}.{} ({})"
    ).format(
        sql.Identifier("raw"),
        sql.Identifier(table_name),
        sql.SQL(", ").join(column_definitions),
    )

    db.execute(create_query, commit=False)

    db.cursor.execute(
        """
        SELECT
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = %s
          AND table_name = %s
        ORDER BY ordinal_position;
        """,
        ("raw", table_name),
    )

    actual_schema = db.cursor.fetchall()
    actual_columns = [
        column_name
        for column_name, _ in actual_schema
    ]

    if actual_columns != expected_columns:
        raise SchemaValidationError(
            f"Existing raw.{table_name} columns "
            f"{actual_columns} do not match the contract "
            f"{expected_columns}. Apply an explicit migration."
        )

    expected_schema = [
        (
            column_name,
            POSTGRES_TYPE_NAMES[postgres_type],
        )
        for column_name, postgres_type
        in RAW_TABLE_SCHEMAS[table_name].items()
    ]

    if actual_schema != expected_schema:
        raise SchemaValidationError(
            f"Existing raw.{table_name} schema "
            f"{actual_schema} does not match the contract "
            f"{expected_schema}. Apply an explicit migration."
        )