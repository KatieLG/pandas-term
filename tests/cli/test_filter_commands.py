import json
from pathlib import Path

import pytest
from pytest_snapshot.plugin import Snapshot
from typer.testing import CliRunner

from pandas_term.main import app
from tests.conftest import InputMode, get_input_args

runner = CliRunner()

FILTER_COMMANDS = {
    "query_simple": ["query", "stock > 30"],
    "query_complex": ["query", "price > 1.4 and category == 'Fruit'"],
    "head_default": ["head"],
    "head_n3": ["head", "--n", "3"],
    "tail_default": ["tail"],
    "tail_n2": ["tail", "--n", "2"],
    "dropna_any": ["dropna"],
    "dropna_subset_price": ["dropna", "--subset", "price"],
    "dropna_subset_category": ["dropna", "--subset", "category"],
    "dropna_subset_multiple": ["dropna", "--subset", "price,category"],
    "duplicated_all": ["duplicated"],
    "duplicated_keep_last": ["duplicated", "--keep", "last"],
    "duplicated_keep_false": ["duplicated", "--keep", "False"],
    "duplicated_subset_name": ["duplicated", "--subset", "name"],
}


@pytest.mark.parametrize("csv_file", ["sample_csv_file", "empty_csv_file"], indirect=True)
@pytest.mark.parametrize("input_mode", ["file_arg", "stdin_explicit", "stdin_implicit"])
def test_filter_commands(
    csv_file: Path,
    input_mode: InputMode,
    snapshot: Snapshot,
) -> None:
    snapshot.snapshot_dir = "tests/cli/snapshots/filter"
    input_args, stdin = get_input_args(csv_file, input_mode)

    results = {}
    for test_name, args in FILTER_COMMANDS.items():
        result = runner.invoke(app, [*args, *input_args, "--json"], input=stdin)
        assert result.exit_code == 0, f"{test_name} failed: {result.stdout}"
        results[test_name] = json.loads(result.stdout)

    snapshot.assert_match(json.dumps(results, indent=2), f"filter_{csv_file.stem}.json")
