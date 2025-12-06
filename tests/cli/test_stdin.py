"""Tests for stdin input handling."""

import json

import pandas as pd
import pytest
from typer.testing import CliRunner

from pandas_term.main import app

runner = CliRunner()


@pytest.fixture
def csv_content(sample_df: pd.DataFrame) -> str:
    """Return sample dataframe as CSV string."""
    return sample_df.to_csv(index=False)


@pytest.mark.parametrize(
    "command,args",
    [
        ("select", ["name,age"]),
        ("head", ["--n", "3"]),
        ("tail", ["--n", "2"]),
        ("query", ["age > 30"]),
        ("sort", ["age"]),
        ("drop", ["salary"]),
        ("describe", []),
        ("shape", []),
        ("columns", []),
    ],
)
def test_stdin_input(command: str, args: list[str], csv_content: str) -> None:
    """Test that commands work with stdin input."""
    result = runner.invoke(app, [command, *args, "-"], input=csv_content)
    assert result.exit_code == 0, f"{command} failed with stdin: {result.stdout}"


def test_stdin_select_json_output(csv_content: str) -> None:
    """Test select with stdin and JSON output."""
    result = runner.invoke(app, ["select", "name,age", "-", "--json"], input=csv_content)
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert len(data) == 5
    assert all("name" in row and "age" in row for row in data)


def test_stdin_query(csv_content: str) -> None:
    """Test query with stdin input."""
    result = runner.invoke(app, ["query", "age > 30", "-", "--json"], input=csv_content)
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert all(row["age"] > 30 for row in data)


def test_stdin_groupby(csv_content: str) -> None:
    """Test groupby with stdin input."""
    result = runner.invoke(
        app,
        ["groupby", "city", "-", "--col", "salary", "--agg", "sum", "--json"],
        input=csv_content,
    )
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert len(data) > 0


def test_stdin_value_counts(csv_content: str) -> None:
    """Test value-counts with stdin input."""
    result = runner.invoke(app, ["value-counts", "city", "-", "--json"], input=csv_content)
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert len(data) > 0
