from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

# Add ETL folder to Python path
ETL_PATH = "/opt/airflow/etl"
sys.path.append(ETL_PATH)

from extract import extract_customers
from load import load_customers
from transform import transform_customers
from validate import validate_customers

# Default arguments
default_args = {
    "owner": "Dipayan",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="customer_etl_pipeline",
    default_args=default_args,
    description="End-to-End Customer ETL Pipeline using Airflow and Snowflake",
    start_date=datetime(2025, 1, 1),

    # Schedule
    schedule="@daily",

    # Don't run old missed DAGs
    catchup=False,

    # Limit parallel active runs
    max_active_runs=1,

    # Tags
    tags=["ETL", "Snowflake", "Python", "Data Engineering"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_customers",
        python_callable=extract_customers,
    )

    load_task = PythonOperator(
        task_id="load_customers",
        python_callable=load_customers,
    )

    transform_task = PythonOperator(
        task_id="transform_customers",
        python_callable=transform_customers,
    )

    validate_task = PythonOperator(
        task_id="validate_customers",
        python_callable=validate_customers,
    )

    extract_task >> load_task >> transform_task >> validate_task