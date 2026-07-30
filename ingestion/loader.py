import pandas as pd
from psycopg2 import sql
from psycopg2.extras import execute_values


def clean_dataframe(dataframe):
    cleaned_dataframe = dataframe.copy()

    return cleaned_dataframe.where(
        pd.notnull(cleaned_dataframe),
        None,
    )


def convert_value(value):
    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    return value


def truncate_raw_table(db, table_name):
    query = sql.SQL(
        "TRUNCATE TABLE {}.{}"
    ).format(
        sql.Identifier("raw"),
        sql.Identifier(table_name),
    )

    db.execute(query, commit=False)


def insert_dataframe_to_raw(
    db,
    dataframe,
    table_name,
):
    dataframe = clean_dataframe(dataframe)

    if dataframe.empty:
        return 0

    columns = list(dataframe.columns)

    query = sql.SQL(
        "INSERT INTO {}.{} ({}) VALUES %s"
    ).format(
        sql.Identifier("raw"),
        sql.Identifier(table_name),
        sql.SQL(", ").join(
            sql.Identifier(column)
            for column in columns
        ),
    )

    values = [
        tuple(
            convert_value(value)
            for value in row
        )
        for row in dataframe.to_numpy()
    ]

    execute_values(
        db.cursor,
        query.as_string(db.conn),
        values,
        page_size=1000,
    )

    return len(values)