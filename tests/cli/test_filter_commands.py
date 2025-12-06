"""Snapshot tests for filter CLI commands."""

import json
from pathlib import Path

import pandas as pd
from pytest_snapshot.plugin import Snapshot
from typer.testing import CliRunner

from pandas_term.main import app

runner = CliRunner()


FILTER_COMMANDS = {
    "query_simple": ["query", "age > 30"],
    "query_complex": ["query", "age > 30 and city == 'NYC'"],
    "head_default": ["head"],
    "head_n3": ["head", "--n", "3"],
    "tail_default": ["tail"],
    "tail_n2": ["tail", "--n", "2"],
}

EMPTY_FILTER_COMMANDS = {
    "empty_query": ["query", "age > 30"],
    "empty_head": ["head"],
    "empty_tail": ["tail"],
}


DROPNA_COMMANDS = {
    "dropna_any": ["dropna"],
    "dropna_subset_age": ["dropna", "--subset", "age"],
    "dropna_subset_city": ["dropna", "--subset", "city"],
    "dropna_subset_multiple": ["dropna", "--subset", "age,city"],
}


def test_filter_commands(tmp_path: Path, sample_df: pd.DataFrame, snapshot: Snapshot) -> None:
    snapshot.snapshot_dir = "tests/cli/snapshots/filter"

    csv_file = tmp_path / "test.csv"
    sample_df.to_csv(csv_file, index=False)

    results = {}
    for test_name, commands in FILTER_COMMANDS.items():
        result = runner.invoke(app, [*commands, str(csv_file), "--json"])
        assert result.exit_code == 0, f"{test_name} failed: {result.stderr}"
        results[test_name] = json.loads(result.stdout)

    snapshot.assert_match(json.dumps(results, indent=2), "filter_commands.json")


def test_dropna_commands(
    tmp_path: Path, sample_df_with_nulls: pd.DataFrame, snapshot: Snapshot
) -> None:
    snapshot.snapshot_dir = "tests/cli/snapshots/filter"

    csv_file = tmp_path / "test_nulls.csv"
    sample_df_with_nulls.to_csv(csv_file, index=False)

    results = {}
    for test_name, commands in DROPNA_COMMANDS.items():
        result = runner.invoke(app, [*commands, str(csv_file), "--json"])
        assert result.exit_code == 0, f"{test_name} failed: {result.stderr}"
        results[test_name] = json.loads(result.stdout)

    snapshot.assert_match(json.dumps(results, indent=2), "dropna_commands.json")


def test_empty_filter_commands(empty_csv_file: Path, snapshot: Snapshot) -> None:
    snapshot.snapshot_dir = "tests/cli/snapshots/filter"

    results = {}
    for test_name, commands in EMPTY_FILTER_COMMANDS.items():
        result = runner.invoke(app, [*commands, str(empty_csv_file), "--json"])
        assert result.exit_code == 0, f"{test_name} failed: {result.stderr}"
        results[test_name] = json.loads(result.stdout)

    snapshot.assert_match(json.dumps(results, indent=2), "empty_filter_commands.json")
