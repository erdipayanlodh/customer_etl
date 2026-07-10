import os
import pandas as pd

from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook


def load_customers():

    print("=" * 60)
    print("Loading Customers into Snowflake")
    print("=" * 60)

    # CSV Path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "raw", "customers.csv")

    df = pd.read_csv(csv_path)

    print(f"Found {len(df)} customers")

    # Airflow Connection
    hook = SnowflakeHook(
        snowflake_conn_id="snowflake_default"
    )

    conn = hook.get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
        CURRENT_USER(),
        CURRENT_ROLE(),
        CURRENT_DATABASE(),
        CURRENT_SCHEMA(),
        CURRENT_WAREHOUSE();
     """)

    print(cursor.fetchone())

    # Remove previous data
    cursor.execute("""
        TRUNCATE TABLE CUSTOMER_DB.BRONZE.CUSTOMER_RAW
    """)

    # Insert rows
    rows = list(df.itertuples(index=False, name=None))

    cursor.executemany(
        """
        INSERT INTO CUSTOMER_DB.BRONZE.CUSTOMER_RAW
        (ID, NAME, USERNAME, EMAIL, PHONE, WEBSITE)
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        rows,
    )

    conn.commit()

    print(f"\nLoaded {len(rows)} rows successfully!")

    cursor.execute("""
        SELECT COUNT(*)
        FROM CUSTOMER_DB.BRONZE.CUSTOMER_RAW
    """)

    print("Rows inside Snowflake:", cursor.fetchone()[0])

    cursor.close()
    conn.close()


if __name__ == "__main__":
    load_customers()