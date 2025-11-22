"""Test configuration and fixtures."""

from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Sample dataframe for testing."""
    return pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [25, 30, 35, 40, 45],
            "city": ["NYC", "LA", "Chicago", "NYC", "LA"],
            "salary": [50000, 60000, 70000, 80000, 90000],
            "department": [
                "Engineering",
                "Sales",
                "Engineering",
                "Sales",
                "Engineering",
            ],
        }
    )


@pytest.fixture
def sample_df_with_nulls() -> pd.DataFrame:
    """Sample dataframe with null values for testing."""
    return pd.DataFrame(
        {
            "name": ["Alice", "Bob", None, "David", "Eve"],
            "age": [25, 30, 35, None, 45],
            "city": ["NYC", None, "Chicago", "NYC", "LA"],
            "salary": [50000, 60000, 70000, 80000, None],
        }
    )


@pytest.fixture
def sample_csv_file(tmp_path: Path, sample_df: pd.DataFrame) -> Path:
    """Create a temporary CSV file for testing."""
    csv_path = tmp_path / "test.csv"
    sample_df.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def sample_excel_file(tmp_path: Path, sample_df: pd.DataFrame) -> Path:
    """Create a temporary Excel file for testing."""
    excel_path = tmp_path / "test.xlsx"
    sample_df.to_excel(excel_path, index=False)
    return excel_path


@pytest.fixture
def sample_json_file(tmp_path: Path, sample_df: pd.DataFrame) -> Path:
    """Create a temporary JSON file for testing."""
    json_path = tmp_path / "test.json"
    sample_df.to_json(json_path, orient="records", indent=2)
    return json_path
