"""Snapshot tests for filter CLI commands."""

import json
from pathlib import Path

import pandas as pd
import pytest
from pytest_snapshot.plugin import Snapshot
from typer.testing import CliRunner

from pandas_cli.main import app

runner = CliRunner()


@pytest.fixture
def test_data() -> pd.DataFrame:
    """Standard test dataset for filter command tests."""
    return pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [25, 30, 35, 40, 45],
            "city": ["NYC", "LA", "Chicago", "NYC", "LA"],
            "salary": [50000, 60000, 70000, 80000, 90000],
        }
    )


@pytest.fixture
def test_data_with_nulls() -> pd.DataFrame:
    """Test dataset with null values for dropna tests."""
    return pd.DataFrame(
        {
            "name": ["Alice", "Bob", None, "David", "Eve"],
            "age": [25, 30, 35, None, 45],
            "city": ["NYC", None, "Chicago", "NYC", "LA"],
        }
    )


FILTER_COMMANDS = {
    "query_simple": ["query", "age > 30"],
    "query_complex": ["query", "age > 30 and city == 'NYC'"],
    "head_default": ["head"],
    "head_n3": ["head", "--n", "3"],
    "tail_default": ["tail"],
    "tail_n2": ["tail", "--n", "2"],
    "sample_n3_seed42": ["sample", "--n", "3", "--seed", "42"],
    "sample_frac05_seed42": ["sample", "--frac", "0.5", "--seed", "42"],
}


DROPNA_COMMANDS = {
    "dropna_any": ["dropna"],
    "dropna_column_age": ["dropna", "--column", "age"],
    "dropna_column_city": ["dropna", "--column", "city"],
}


def test_filter_commands(tmp_path: Path, test_data: pd.DataFrame, snapshot: Snapshot) -> None:
    """Test all filter commands against snapshots."""
    snapshot.snapshot_dir = "tests/cli/snapshots/filter"

    csv_file = tmp_path / "test.csv"
    test_data.to_csv(csv_file, index=False)

    results = {}
    for test_name, command in FILTER_COMMANDS.items():
        result = runner.invoke(app, command + [str(csv_file)])
        results[test_name] = {
            "exit_code": result.exit_code,
            "stdout": result.stdout,
            "stderr": result.stderr if result.stderr else None,
        }

    snapshot.assert_match(json.dumps(results, indent=4, ensure_ascii=False), "filter_commands.json")


def test_dropna_commands(
    tmp_path: Path, test_data_with_nulls: pd.DataFrame, snapshot: Snapshot
) -> None:
    """Test dropna commands against snapshots."""
    snapshot.snapshot_dir = "tests/cli/snapshots/filter"

    csv_file = tmp_path / "test_nulls.csv"
    test_data_with_nulls.to_csv(csv_file, index=False)

    results = {}
    for test_name, command in DROPNA_COMMANDS.items():
        result = runner.invoke(app, command + [str(csv_file)])
        results[test_name] = {
            "exit_code": result.exit_code,
            "stdout": result.stdout,
            "stderr": result.stderr if result.stderr else None,
        }

    snapshot.assert_match(json.dumps(results, indent=4, ensure_ascii=False), "dropna_commands.json")
