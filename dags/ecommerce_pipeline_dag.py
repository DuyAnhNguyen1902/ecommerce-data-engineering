from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "duyanh",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="ecommerce_data_pipeline",
    default_args=default_args,
    description="Run ecommerce data pipeline",
    start_date=datetime(2026, 7, 8),
    schedule=None,
    catchup=False,
    tags=["ecommerce", "data-engineering"],
) as dag:

    run_pipeline = BashOperator(
        task_id="run_main_pipeline",
        bash_command="cd /opt/airflow/project && python main.py",
    )