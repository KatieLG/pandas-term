"""Snapshot tests for aggregate CLI commands."""

import json
from pathlib import Path

import pandas as pd
from pytest_snapshot.plugin import Snapshot
from typer.testing import CliRunner

from pandas_term.main import app

runner = CliRunner()


AGGREGATE_COMMANDS = {
    "value_counts_city": ["value-counts", "city"],
    "value_counts_department": ["value-counts", "department"],
    "value_counts_normalized": ["value-counts", "city", "--normalize"],
    "value_counts_multi_col": ["value-counts", "city,department"],
    "value_counts_multi_col_normalized": ["value-counts", "city,department", "--normalize"],
    "groupby_single_col_sum": ["groupby", "city", "--col", "salary", "--agg", "sum"],
    "groupby_single_col_mean": ["groupby", "department", "--col", "age", "--agg", "mean"],
    "groupby_single_col_count": ["groupby", "city", "--col", "age", "--agg", "count"],
    "groupby_multi_col": ["groupby", "city,department", "--col", "salary", "--agg", "sum"],
    "groupby_multi_agg_col": ["groupby", "city", "--col", "salary,age", "--agg", "sum"],
}


def test_aggregate_commands(tmp_path: Path, sample_df: pd.DataFrame, snapshot: Snapshot) -> None:
    snapshot.snapshot_dir = "tests/cli/snapshots/aggregate"

    csv_file = tmp_path / "test.csv"
    sample_df.to_csv(csv_file, index=False)

    results = {}
    for test_name, commands in AGGREGATE_COMMANDS.items():
        result = runner.invoke(app, [*commands, str(csv_file), "--json"])
        assert result.exit_code == 0, f"{test_name} failed: {result.stderr}"
        results[test_name] = json.loads(result.stdout)

    snapshot.assert_match(json.dumps(results, indent=2), "aggregate_commands.json")
