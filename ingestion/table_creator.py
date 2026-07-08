import pandas as pd


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
        columns.append(f'"{col}" {pg_type}')

    columns_sql = ",\n    ".join(columns)

    query = f"""
    CREATE TABLE IF NOT EXISTS raw."{table_name}" (
        {columns_sql}
    );
    """

    db.execute(query)