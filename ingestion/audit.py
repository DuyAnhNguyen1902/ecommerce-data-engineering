from config.logging_config import logger


VALID_ETL_STATUSES = {
    "SUCCESS",
    "FAILED",
}


def insert_etl_log(
    db,
    job_name,
    table_name,
    start_time,
    end_time,
    status,
    rows_loaded=0,
    error_message=None,
    commit=True,
):
    normalized_status = status.strip().upper()

    if normalized_status not in VALID_ETL_STATUSES:
        raise ValueError(
            f"Invalid ETL status: {status!r}. "
            f"Expected one of {sorted(VALID_ETL_STATUSES)}."
        )

    if rows_loaded < 0:
        raise ValueError("rows_loaded cannot be negative.")

    query = """
        INSERT INTO metadata.etl_job_log (
            job_name,
            table_name,
            start_time,
            end_time,
            status,
            rows_loaded,
            error_message
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    params = (
        job_name,
        table_name,
        start_time,
        end_time,
        normalized_status,
        rows_loaded,
        error_message,
    )

    db.execute(
        query,
        params=params,
        commit=commit,
    )

    logger.info(
        "ETL audit recorded | job=%s | table=%s | "
        "status=%s | rows=%s",
        job_name,
        table_name,
        normalized_status,
        rows_loaded,
    )