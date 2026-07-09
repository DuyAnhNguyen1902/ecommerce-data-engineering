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
    description="Ecommerce ELT pipeline: raw -> warehouse -> mart",
    schedule=None,
    start_date=datetime(2026, 7, 1),
    catchup=False,
    tags=["ecommerce", "elt", "data-engineering"],
) as dag:

    load_raw = BashOperator(
        task_id="load_raw",
        bash_command="""
        cd /opt/airflow/project &&
        python -m ingestion.load_raw
        """,
    )

    load_warehouse = BashOperator(
        task_id="load_warehouse",
        bash_command="""
        cd /opt/airflow/project &&
        python -m warehouse.load_warehouse
        """,
    )

    load_mart = BashOperator(
        task_id="load_mart",
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
    load_raw >> load_warehouse >> load_mart >> quality_check