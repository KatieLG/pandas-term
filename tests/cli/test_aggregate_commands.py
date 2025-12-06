import json
from pathlib import Path

import pytest
from pytest_snapshot.plugin import Snapshot
from typer.testing import CliRunner

from pandas_term.main import app
from tests.conftest import InputMode, get_input_args

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
