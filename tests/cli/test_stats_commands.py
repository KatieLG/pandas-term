import json
from pathlib import Path

import pytest
from pytest_snapshot.plugin import Snapshot
from typer.testing import CliRunner

from pandas_term.main import app
from tests.conftest import InputMode, get_input_args

runner = CliRunner()

STATS_COMMANDS = {
    "describe": ["describe", "--json"],
    "unique_category": ["unique", "category"],
    "unique_aisle": ["unique", "aisle"],
    "shape": ["shape"],
    "columns": ["columns"],
    "dtypes": ["dtypes"],
}


@pytest.mark.parametrize("csv_file", ["sample_csv_file", "empty_csv_file"], indirect=True)
@pytest.mark.parametrize("input_mode", ["file_arg", "stdin_explicit", "stdin_implicit"])
def test_stats_commands(
    csv_file: Path,
    input_mode: InputMode,
    snapshot: Snapshot,
) -> None:
    snapshot.snapshot_dir = "tests/cli/snapshots/stats"
    input_args, stdin = get_input_args(csv_file, input_mode)

    results = {}
    for test_name, args in STATS_COMMANDS.items():
        result = runner.invoke(app, [*args, *input_args], input=stdin)
        assert result.exit_code == 0, f"{test_name} failed: {result.stdout}"
        try:
            results[test_name] = json.loads(result.stdout)
        except json.JSONDecodeError:
            results[test_name] = result.stdout

    snapshot.assert_match(json.dumps(results, indent=2), f"stats_{csv_file.stem}.json")
