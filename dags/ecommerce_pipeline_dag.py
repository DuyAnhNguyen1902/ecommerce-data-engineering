from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "duyanh",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="ecommerce_data_pipeline",
    default_args=default_args,
    description="Ecommerce ETL Pipeline",
    schedule=None,
    start_date=datetime(2026, 7, 1),
    catchup=False,
    tags=["ecommerce", "etl", "postgresql"],
) as dag:

    extract_raw = BashOperator(
        task_id="extract_raw",
        bash_command="""
        cd /opt/airflow/project &&
        python -m ingestion.load_raw
        """,
    )

    warehouse_incremental = BashOperator(
        task_id="warehouse_incremental",
        bash_command="""
        cd /opt/airflow/project &&
        python -m warehouse.load_warehouse
        """,
    )

    mart_refresh = BashOperator(
        task_id="mart_refresh",
        bash_command="""
        cd /opt/airflow/project &&
        python -m mart.load_mart
        """,
    )

    quality_check = BashOperator(
        task_id="quality_check",
        bash_command="""
        cd /opt/airflow/project &&
        python -m quality.data_quality
        """,
    )

    extract_raw >> warehouse_incremental >> mart_refresh >> quality_check