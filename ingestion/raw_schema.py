import re


class SchemaValidationError(ValueError):
    """Raised when source data does not match the Raw schema contract."""


RAW_TABLE_SCHEMAS = {
    "dim_products": {
        "product_id": "TEXT",
        "product_name": "TEXT",
        "category": "TEXT",
        "price": "NUMERIC",
    },
    "fact_orders": {
        "order_id": "TEXT",
        "user_id": "TEXT",
        "created_at": "TIMESTAMPTZ",
        "final_total": "NUMERIC",
        "discount_value": "NUMERIC",
        "status": "TEXT",
        "payment_method": "TEXT",
    },
    "fact_order_items": {
        "order_id": "TEXT",
        "product_id": "TEXT",
        "variant_id": "TEXT",
        "quantity": "INTEGER",
        "price": "NUMERIC",
        "line_total": "NUMERIC",
    },
    "fact_payments": {
        "payment_id": "TEXT",
        "order_id": "TEXT",
        "payment_status": "TEXT",
        "amount_vnd": "NUMERIC",
        "paid_at": "TIMESTAMPTZ",
        "created_at": "TIMESTAMPTZ",
    },
    "fact_reviews": {
        "review_id": "TEXT",
        "product_id": "TEXT",
        "user_id": "TEXT",
        "rating": "NUMERIC",
        "comment": "TEXT",
        "created_at": "TIMESTAMPTZ",
    },
    "fact_product_sales": {
        "product_id": "TEXT",
        "month": "INTEGER",
        "year": "INTEGER",
        "quantity_sold": "INTEGER",
        "revenue": "NUMERIC",
    },
    "dim_inventory_status": {
        "product_id": "TEXT",
        "product_name": "TEXT",
        "variant_id": "TEXT",
        "stock": "INTEGER",
        "is_low_stock": "INTEGER",
        "created_at": "TIMESTAMPTZ",
    },
}


def normalize_identifier(value):
    """
    Convert Excel sheet and column names to snake_case.

    Examples:
        Product ID   -> product_id
        Product_id   -> product_id
        Amount (VND) -> amount_vnd
    """
    normalized = re.sub(
        r"(?<=[a-z0-9])(?=[A-Z])",
        "_",
        str(value).strip(),
    )

    normalized = re.sub(
        r"[^0-9A-Za-z]+",
        "_",
        normalized,
    )

    return normalized.strip("_").lower()


def normalize_and_validate_dataframe(dataframe, table_name):
    if table_name not in RAW_TABLE_SCHEMAS:
        raise SchemaValidationError(
            f"No Raw schema contract exists for {table_name!r}."
        )

    normalized_columns = [
        normalize_identifier(column)
        for column in dataframe.columns
    ]

    if len(normalized_columns) != len(set(normalized_columns)):
        raise SchemaValidationError(
            f"Duplicate columns after normalization in "
            f"{table_name}: {normalized_columns}"
        )

    normalized_dataframe = dataframe.copy()
    normalized_dataframe.columns = normalized_columns

    # Excel may generate empty columns named "Unnamed: N".
    empty_unnamed_columns = [
        column
        for column in normalized_dataframe.columns
        if column.startswith("unnamed_")
        and normalized_dataframe[column].isna().all()
    ]

    normalized_dataframe = normalized_dataframe.drop(
        columns=empty_unnamed_columns
    )

    expected_columns = set(RAW_TABLE_SCHEMAS[table_name])
    actual_columns = set(normalized_dataframe.columns)

    missing_columns = sorted(
        expected_columns - actual_columns
    )
    unexpected_columns = sorted(
        actual_columns - expected_columns
    )

    if missing_columns or unexpected_columns:
        raise SchemaValidationError(
            f"Schema mismatch for raw.{table_name}: "
            f"missing={missing_columns or 'none'}, "
            f"unexpected={unexpected_columns or 'none'}. "
            "Update the schema contract and database migration "
            "intentionally."
        )

    ordered_columns = list(
        RAW_TABLE_SCHEMAS[table_name]
    )

    return normalized_dataframe[ordered_columns]