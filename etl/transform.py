import os
import pandas as pd

from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook


def transform_customers():

    print("=" * 60)
    print("Starting Data Transformation")
    print("=" * 60)

    # Base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # SQL file path
    sql_file = os.path.join(base_dir, "sql", "transformations.sql")

    print("=" * 60)
    print("Current File :", __file__)
    print("Base Dir     :", base_dir)
    print("SQL File     :", sql_file)
    print("Exists       :", os.path.exists(sql_file))
    print("=" * 60)

    # Read SQL
    with open(sql_file, "r") as f:
        sql = f.read()

    # Snowflake Connection
    hook = SnowflakeHook(
        snowflake_conn_id="snowflake_default"
    )

    conn = hook.get_conn()
    cursor = conn.cursor()

    # Execute SQL statements
    for statement in sql.split(";"):
        if statement.strip():
            cursor.execute(statement)

    conn.commit()

    print("Transformation Completed Successfully!")

    # Verify rows
    cursor.execute("""
        SELECT COUNT(*)
        FROM CUSTOMER_DB.ANALYTICS.CUSTOMERS_CLEAN
    """)

    rows = cursor.fetchone()[0]

    print(f"Analytics Table Rows : {rows}")

    # -------------------------------------------------
    # Export cleaned table to processed CSV
    # -------------------------------------------------

    cursor.execute("""
        SELECT *
        FROM CUSTOMER_DB.ANALYTICS.CUSTOMERS_CLEAN
    """)

    data = cursor.fetchall()

    columns = [col[0] for col in cursor.description]

    df = pd.DataFrame(data, columns=columns)

    processed_folder = os.path.join(base_dir, "data", "processed")

    os.makedirs(processed_folder, exist_ok=True)

    processed_file = os.path.join(
        processed_folder,
        "customers_clean.csv"
    )

    df.to_csv(processed_file, index=False)

    print("=" * 60)
    print("Processed CSV Created Successfully!")
    print(processed_file)
    print("=" * 60)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    transform_customers()