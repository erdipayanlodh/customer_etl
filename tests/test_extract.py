import os
import pandas as pd

from etl.extract import extract_customers


def test_extract_returns_dataframe():
    """Check that the function returns a DataFrame."""

    df = extract_customers()

    assert isinstance(df, pd.DataFrame)


def test_dataframe_not_empty():
    """Check that extracted data is not empty."""

    df = extract_customers()

    assert not df.empty


def test_customer_count():
    """Check that exactly 10 customers are extracted."""

    df = extract_customers()

    assert len(df) == 10


def test_required_columns():
    """Check required columns exist."""

    df = extract_customers()

    expected_columns = [
        "id",
        "name",
        "username",
        "email",
        "phone",
        "website",
    ]

    assert list(df.columns) == expected_columns


def test_csv_created():
    """Check that customers.csv exists."""

    extract_customers()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    csv_path = os.path.join(
        project_root,
        "data",
        "raw",
        "customers.csv"
    )

    assert os.path.exists(csv_path)


def test_json_created():
    """Check that customers.json exists."""

    extract_customers()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    json_path = os.path.join(
        project_root,
        "data",
        "raw",
        "customers.json"
    )

    assert os.path.exists(json_path)