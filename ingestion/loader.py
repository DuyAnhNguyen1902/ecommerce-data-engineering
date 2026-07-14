import pandas as pd
from psycopg2 import sql
from psycopg2.extras import execute_values


def clean_dataframe(df):
    df = df.copy()

    df = df.where(pd.notnull(df), None)

    return df


def convert_value(value):
    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    return value


def truncate_raw_table(db, table_name):
    query = sql.SQL("TRUNCATE TABLE {}.{}").format(
        sql.Identifier("raw"),
        sql.Identifier(table_name),
    )
    db.execute(query)


def insert_dataframe_to_raw(db, df, table_name):
    df = clean_dataframe(df)

    columns = list(df.columns)
    columns_sql = sql.SQL(", ").join(map(sql.Identifier, columns))
    query = sql.SQL(
        "INSERT INTO {}.{} ({}) VALUES %s"
    ).format(
        sql.Identifier("raw"),
        sql.Identifier(table_name),
        columns_sql,
    ).as_string(db.conn)

    values = [
        tuple(convert_value(value) for value in row)
        for row in df.to_numpy()
    ]

    execute_values(
        db.cursor,
        query,
        values,
        page_size=1000
    )

    db.conn.commit()
