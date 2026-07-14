import pandas as pd
from psycopg2 import sql


def map_dtype_to_postgres(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "BIGINT"

    if pd.api.types.is_float_dtype(dtype):
        return "NUMERIC"

    if pd.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"

    if pd.api.types.is_datetime64_any_dtype(dtype):
        return "TIMESTAMP"

    return "TEXT"


def create_raw_table(db, df, table_name):
    columns = []

    for col in df.columns:
        pg_type = map_dtype_to_postgres(df[col].dtype)
        columns.append(
            sql.SQL("{} {}").format(sql.Identifier(col), sql.SQL(pg_type))
        )

    columns_sql = sql.SQL(",\n    ").join(columns)

    query = sql.SQL(
        """
        CREATE TABLE IF NOT EXISTS {}.{} (
            {}
        );
        """
    ).format(
        sql.Identifier("raw"),
        sql.Identifier(table_name),
        columns_sql,
    )

    db.execute(query)
