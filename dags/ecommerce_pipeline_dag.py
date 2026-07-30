from datetime import timedelta

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_DIR = "/opt/airflow/project"

default_args = {
    "owner": "duyanh",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(minutes=30),
}


with DAG(
    dag_id="ecommerce_data_pipeline",
    default_args=default_args,
    description=(
        "Load ecommerce data from Excel through "
        "Raw, Warehouse, Mart and Data Quality layers"
    ),
    schedule=None,
    start_date=pendulum.datetime(
        2026,
        7,
        1,
        tz="Asia/Ho_Chi_Minh",
    ),
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=timedelta(hours=1),
    tags=["ecommerce", "etl", "postgresql"],
) as dag:

    load_raw = BashOperator(
        task_id="load_raw",
        bash_command=f"""
            set -euo pipefail
            cd {PROJECT_DIR}
            python -m ingestion.load_raw
        """,
    )

    load_warehouse = BashOperator(
        task_id="load_warehouse",
        bash_command=f"""
            set -euo pipefail
            cd {PROJECT_DIR}
            python -m warehouse.load_warehouse
        """,
    )

    load_mart = BashOperator(
        task_id="load_mart",
        bash_command=f"""
            set -euo pipefail
            cd {PROJECT_DIR}
            python -m mart.load_mart
        """,
    )

    data_quality_check = BashOperator(
        task_id="data_quality_check",
        bash_command=f"""
            set -euo pipefail
            cd {PROJECT_DIR}
            python -m quality.data_quality
        """,
    )

    load_raw >> load_warehouse >> load_mart >> data_quality_check