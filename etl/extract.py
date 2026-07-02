import requests
import pandas as pd
import os
import json


def extract_customers():

    print("=" * 60)
    print("Starting Customer Data Extraction")
    print("=" * 60)

    url = "https://jsonplaceholder.typicode.com/users"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("API Request Failed")

    customers = response.json()

    print(f"Fetched {len(customers)} customers from API")

    # -----------------------------
    # Create data/raw folder
    # -----------------------------

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    raw_path = os.path.join(base_dir, "data", "raw")

    os.makedirs(raw_path, exist_ok=True)

    # -----------------------------
    # Save JSON
    # -----------------------------

    json_path = os.path.join(raw_path, "customers.json")

    with open(json_path, "w") as f:
        json.dump(customers, f, indent=4)

    # -----------------------------
    # Convert to DataFrame
    # -----------------------------

    df = pd.DataFrame(customers)

    df = df[
        [
            "id",
            "name",
            "username",
            "email",
            "phone",
            "website",
        ]
    ]

    csv_path = os.path.join(raw_path, "customers.csv")

    df.to_csv(csv_path, index=False)

    print("\nExtraction Successful!\n")

    print(df.head())

    print("\nCSV Saved :", csv_path)
    print("JSON Saved:", json_path)

    return csv_path


if __name__ == "__main__":
    extract_customers()