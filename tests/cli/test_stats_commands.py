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
    "describe": ["describe", "--json"],
    "info": ["info"],
    "unique_city": ["unique", "city"],
    "unique_department": ["unique", "department"],
    "size": ["size"],
    "shape": ["shape"],
    "columns": ["columns"],
    "memory": ["memory"],
    "memory_deep": ["memory", "--deep"],
}


def test_stats_commands(tmp_path: Path, test_data: pd.DataFrame, snapshot: Snapshot) -> None:
    """Test stats commands against snapshots."""
    snapshot.snapshot_dir = "tests/cli/snapshots/stats"

    csv_file = tmp_path / "test.csv"
    test_data.to_csv(csv_file, index=False)

    results = {}
    for test_name, command in STATS_COMMANDS.items():
        result = runner.invoke(app, command + [str(csv_file)])
        assert result.exit_code == 0, f"{test_name} failed: {result.stderr}"
        try:
            results[test_name] = json.loads(result.stdout)
        except json.JSONDecodeError:
            results[test_name] = result.stdout

    snapshot.assert_match(json.dumps(results, indent=2), "stats_commands.json")
