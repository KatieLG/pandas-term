"""Snapshot tests for aggregate CLI commands."""

import json
from pathlib import Path

import pandas as pd
import pytest
from pytest_snapshot.plugin import Snapshot
from typer.testing import CliRunner

from pandas_term.main import app

runner = CliRunner()


@pytest.fixture
def test_data() -> pd.DataFrame:
    """Standard test dataset for aggregate command tests."""
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


AGGREGATE_COMMANDS = {
    "value_counts_city": ["value-counts", "--json", "city"],
    "value_counts_department": ["value-counts", "--json", "department"],
    "value_counts_normalized": ["value-counts", "--json", "city", "--normalize"],
    "groupby_single_col_sum": ["groupby", "--json", "city", "--col", "salary", "--agg", "sum"],
    "groupby_single_col_mean": ["groupby", "--json", "department", "--col", "age", "--agg", "mean"],
    "groupby_single_col_count": ["groupby", "--json", "city", "--col", "age", "--agg", "count"],
    "groupby_multi_col": [
        "groupby",
        "--json",
        "city,department",
        "--col",
        "salary",
        "--agg",
        "sum",
    ],
}


def test_aggregate_commands(tmp_path: Path, test_data: pd.DataFrame, snapshot: Snapshot) -> None:
    """Test aggregate commands against snapshots."""
    snapshot.snapshot_dir = "tests/cli/snapshots/aggregate"

    csv_file = tmp_path / "test.csv"
    test_data.to_csv(csv_file, index=False)

    results = {}
    for test_name, commands in AGGREGATE_COMMANDS.items():
        result = runner.invoke(app, [*commands, str(csv_file)])
        assert result.exit_code == 0, f"{test_name} failed: {result.stderr}"
        try:
            results[test_name] = json.loads(result.stdout)
        except json.JSONDecodeError:
            results[test_name] = result.stdout

    snapshot.assert_match(json.dumps(results, indent=2), "aggregate_commands.json")
