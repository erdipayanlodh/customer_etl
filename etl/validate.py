import os
import pandas as pd

from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook


def validate_customers():

    print("=" * 60)
    print("Starting Data Validation")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    hook = SnowflakeHook(
        snowflake_conn_id="snowflake_default"
    )

    conn = hook.get_conn()
    cursor = conn.cursor()

    # Check total rows
    cursor.execute("""
        SELECT COUNT(*)
        FROM CUSTOMER_DB.ANALYTICS.CUSTOMERS_CLEAN
    """)

    total_rows = cursor.fetchone()[0]

    print(f"Total Rows : {total_rows}")

    # Check duplicate IDs
    cursor.execute("""
        SELECT COUNT(*) - COUNT(DISTINCT ID)
        FROM CUSTOMER_DB.ANALYTICS.CUSTOMERS_CLEAN
    """)

    duplicates = cursor.fetchone()[0]

    print(f"Duplicate IDs : {duplicates}")

    if duplicates == 0:
        print("No duplicate records found.")
    else:
        raise Exception("Duplicate records found!")

    # Export processed CSV
    cursor.execute("""
        SELECT *
        FROM CUSTOMER_DB.ANALYTICS.CUSTOMERS_CLEAN
    """)

    data = cursor.fetchall()

    columns = [col[0] for col in cursor.description]

    df = pd.DataFrame(data, columns=columns)

    processed_folder = os.path.join(base_dir, "data", "processed")

    os.makedirs(processed_folder, exist_ok=True)

    output_file = os.path.join(
        processed_folder,
        "customers_clean.csv"
    )

    df.to_csv(output_file, index=False)

    print(f"Processed CSV saved to: {output_file}")

    print("=" * 60)
    print("Validation Successful")
    print("=" * 60)

    cursor.close()
    conn.close()