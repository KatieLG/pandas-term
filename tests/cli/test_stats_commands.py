"""Snapshot tests for stats CLI commands."""

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
    """Standard test dataset for stats command tests."""
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


STATS_COMMANDS = {
    "describe": ["describe"],
    "info": ["info"],
    "value_counts_city": ["value-counts", "city"],
    "value_counts_department": ["value-counts", "department"],
    "value_counts_normalized": ["value-counts", "city", "--normalize"],
    "groupby_single_col_sum": ["groupby", "city", "--col", "salary", "--agg", "sum"],
    "groupby_single_col_mean": ["groupby", "department", "--col", "age", "--agg", "mean"],
    "groupby_single_col_count": ["groupby", "city", "--col", "age", "--agg", "count"],
    "groupby_multi_col": ["groupby", "city,department", "--col", "salary", "--agg", "sum"],
    "unique_city": ["unique", "city"],
    "unique_department": ["unique", "department"],
}


def test_stats_commands(tmp_path: Path, test_data: pd.DataFrame, snapshot: Snapshot) -> None:
    """Test all stats commands against snapshots."""
    snapshot.snapshot_dir = "tests/cli/snapshots/stats"

    csv_file = tmp_path / "test.csv"
    test_data.to_csv(csv_file, index=False)

    results = {}
    for test_name, command in STATS_COMMANDS.items():
        result = runner.invoke(app, command + [str(csv_file)])
        results[test_name] = {
            "exit_code": result.exit_code,
            "stdout": result.stdout,
            "stderr": result.stderr if result.stderr else None,
        }

    snapshot.assert_match(json.dumps(results, indent=4, ensure_ascii=False), "stats_commands.json")
