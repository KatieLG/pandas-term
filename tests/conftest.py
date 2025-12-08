"""Test configuration and fixtures."""

from pathlib import Path
from typing import Literal, TypeAlias

import pandas as pd
import pytest

InputMode: TypeAlias = Literal["file_arg", "stdin_explicit", "stdin_implicit"]


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "David", "Alice", None],
            "age": [25, 30, 35, None, 25, 40],
            "city": ["NYC", None, "Chicago", "NYC", "NYC", "LA"],
            "salary": [50000, 60000, 70000, 80000, 50000, None],
            "department": ["Engineering", "Sales", "Engineering", "Sales", "Engineering", "Sales"],
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


@pytest.fixture
def sample_tsv_file(tmp_path: Path, sample_df: pd.DataFrame) -> Path:
    """Create a temporary TSV file for testing."""
    tsv_path = tmp_path / "test.tsv"
    sample_df.to_csv(tsv_path, index=False, sep="\t")
    return tsv_path


@pytest.fixture
def sample_parquet_file(tmp_path: Path, sample_df: pd.DataFrame) -> Path:
    """Create a temporary Parquet file for testing."""
    parquet_path = tmp_path / "test.parquet"
    sample_df.to_parquet(parquet_path, index=False)
    return parquet_path


@pytest.fixture
def empty_df() -> pd.DataFrame:
    """Empty dataframe with columns but no rows."""
    return pd.DataFrame({"name": [], "age": [], "city": [], "salary": [], "department": []})


@pytest.fixture
def empty_csv_file(tmp_path: Path, empty_df: pd.DataFrame) -> Path:
    """Create a temporary empty CSV file for testing."""
    csv_path = tmp_path / "empty.csv"
    empty_df.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def csv_file(request: pytest.FixtureRequest) -> Path:
    """Indirect fixture that resolves to the requested CSV file fixture."""
    return request.getfixturevalue(request.param)


def get_input_args(csv_file: Path, input_mode: InputMode) -> tuple[list[str], str | None]:
    """Return (cli_args, stdin_data) for the given input mode."""
    if input_mode == "file_arg":
        return [str(csv_file)], None
    if input_mode == "stdin_explicit":
        return ["-"], csv_file.read_text()
    if input_mode == "stdin_implicit":
        return [], csv_file.read_text()
    raise ValueError(f"Unknown input mode: {input_mode}")
