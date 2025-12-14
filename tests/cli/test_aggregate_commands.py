import json
from pathlib import Path

import pytest
from pytest_snapshot.plugin import Snapshot
from typer.testing import CliRunner

from pandas_term.main import app
from tests.conftest import InputMode, get_input_args

runner = CliRunner()

AGGREGATE_COMMANDS = {
    "value_counts_category": ["value-counts", "category"],
    "value_counts_aisle": ["value-counts", "aisle"],
    "value_counts_normalized": ["value-counts", "category", "--normalize"],
    "value_counts_multi_col": ["value-counts", "category,aisle"],
    "value_counts_multi_col_normalized": ["value-counts", "category,aisle", "--normalize"],
    "groupby_single_col_sum": ["groupby", "category", "--col", "stock", "--agg", "sum"],
    "groupby_single_col_mean": ["groupby", "aisle", "--col", "price", "--agg", "mean"],
    "groupby_single_col_count": ["groupby", "category", "--col", "price", "--agg", "count"],
    "groupby_multi_col": ["groupby", "category,aisle", "--col", "stock", "--agg", "sum"],
    "groupby_multi_agg_col": ["groupby", "category", "--col", "stock,price", "--agg", "sum"],
}


@pytest.mark.parametrize("csv_file", ["sample_csv_file", "empty_csv_file"], indirect=True)
@pytest.mark.parametrize("input_mode", ["file_arg", "stdin_explicit", "stdin_implicit"])
def test_aggregate_commands(
    csv_file: Path,
    input_mode: InputMode,
    snapshot: Snapshot,
) -> None:
    snapshot.snapshot_dir = "tests/cli/snapshots/aggregate"
    input_args, stdin = get_input_args(csv_file, input_mode)

    results = {}
    for test_name, args in AGGREGATE_COMMANDS.items():
        result = runner.invoke(app, [*args, *input_args, "--json"], input=stdin)
        assert result.exit_code == 0, f"{test_name} failed: {result.stdout}"
        results[test_name] = json.loads(result.stdout)

    snapshot.assert_match(json.dumps(results, indent=2), f"aggregate_{csv_file.stem}.json")
