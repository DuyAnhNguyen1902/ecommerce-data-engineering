def insert_etl_log(
    db,
    job_name,
    table_name,
    start_time,
    end_time,
    status,
    rows_loaded=0,
    error_message=None
):
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

    db.cursor.execute(
        query,
        (
            job_name,
            table_name,
            start_time,
            end_time,
            status,
            rows_loaded,
            error_message
        )
    )

    db.conn.commit()