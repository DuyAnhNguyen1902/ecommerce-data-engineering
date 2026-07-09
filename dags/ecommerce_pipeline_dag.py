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
    description="Load latest Excel export into PostgreSQL raw schema",
    schedule=None,
    start_date=datetime(2026, 7, 1),
    catchup=False,
    tags=["ecommerce", "etl"],
) as dag:

    load_raw = BashOperator(
        task_id="load_raw_from_excel",
        bash_command="""
        cd /opt/airflow/project &&
        python -m ingestion.load_raw
        """,
    )