"""Snapshot tests for stats CLI commands."""

import json
from pathlib import Path

import pandas as pd
from pytest_snapshot.plugin import Snapshot
from typer.testing import CliRunner

from pandas_term.main import app

runner = CliRunner()


STATS_COMMANDS = {
    "describe": ["describe", "--json"],
    "unique_city": ["unique", "city"],
    "unique_department": ["unique", "department"],
    "shape": ["shape"],
    "columns": ["columns"],
    "dtypes": ["dtypes"],
}

EMPTY_STATS_COMMANDS = {
    "empty_shape": ["shape"],
    "empty_columns": ["columns"],
    "empty_dtypes": ["dtypes"],
}


def test_stats_commands(tmp_path: Path, sample_df: pd.DataFrame, snapshot: Snapshot) -> None:
    """Test stats commands against snapshots."""
    snapshot.snapshot_dir = "tests/cli/snapshots/stats"

    csv_file = tmp_path / "test.csv"
    sample_df.to_csv(csv_file, index=False)

    results = {}
    for test_name, commands in STATS_COMMANDS.items():
        result = runner.invoke(app, [*commands, str(csv_file)])
        assert result.exit_code == 0, f"{test_name} failed: {result.stderr}"
        try:
            results[test_name] = json.loads(result.stdout)
        except json.JSONDecodeError:
            results[test_name] = result.stdout

    snapshot.assert_match(json.dumps(results, indent=2), "stats_commands.json")


def test_empty_stats_commands(empty_csv_file: Path, snapshot: Snapshot) -> None:
    """Test stats commands on empty dataframe."""
    snapshot.snapshot_dir = "tests/cli/snapshots/stats"

    results = {}
    for test_name, commands in EMPTY_STATS_COMMANDS.items():
        result = runner.invoke(app, [*commands, str(empty_csv_file)])
        assert result.exit_code == 0, f"{test_name} failed: {result.stderr}"
        results[test_name] = result.stdout

    snapshot.assert_match(json.dumps(results, indent=2), "empty_stats_commands.json")
