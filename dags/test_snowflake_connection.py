from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from datetime import datetime


def test_connection():
    hook = SnowflakeHook(snowflake_conn_id="snowflake_default")

    conn = hook.get_conn()

    cur = conn.cursor()

    cur.execute("""
        SELECT
            CURRENT_USER(),
            CURRENT_DATABASE(),
            CURRENT_SCHEMA(),
            CURRENT_WAREHOUSE()
    """)

    result = cur.fetchone()

    print("=" * 50)
    print("Snowflake Connection Successful")
    print("=" * 50)
    print(result)

    cur.close()
    conn.close()


with DAG(
    dag_id="test_snowflake_connection",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    schedule=None,
) as dag:

    PythonOperator(
        task_id="test_connection",
        python_callable=test_connection,
    )