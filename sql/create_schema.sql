CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE SCHEMA IF NOT EXISTS mart;
CREATE SCHEMA IF NOT EXISTS metadata;

CREATE TABLE IF NOT EXISTS metadata.etl_job_log (
    log_id SERIAL PRIMARY KEY,
    job_name TEXT,
    table_name TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status TEXT,
    rows_loaded BIGINT,
    error_message TEXT
);