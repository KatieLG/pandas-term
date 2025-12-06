import json
from pathlib import Path

import pandas as pd
import pytest
from pytest_snapshot.plugin import Snapshot
from typer.testing import CliRunner

from pandas_term.main import app
from tests.conftest import InputMode, get_input_args

runner = CliRunner()

TRANSFORM_COMMANDS = {
    "select_single": ["select", "name"],
    "select_multiple": ["select", "name,age,city"],
    "drop_single": ["drop", "salary"],
    "drop_multiple": ["drop", "city,salary"],
    "sort_single_asc": ["sort", "age", "--ascending"],
    "sort_single_desc": ["sort", "age", "--descending"],
    "sort_multiple_asc": ["sort", "city,age", "--ascending"],
    "sort_multiple_desc": ["sort", "city,age", "--descending"],
    "rename_single": ["rename", "name:full_name"],
    "rename_multiple": ["rename", "name:full_name,age:years"],
    "dedup_all": ["dedup"],
    "dedup_subset_single": ["dedup", "--subset", "name"],
    "dedup_subset_multiple": ["dedup", "--subset", "name,age"],
}


@pytest.mark.parametrize("csv_file", ["sample_csv_file", "empty_csv_file"], indirect=True)
@pytest.mark.parametrize("input_mode", ["file_arg", "stdin_explicit", "stdin_implicit"])
def test_transform_commands(
    csv_file: Path,
    input_mode: InputMode,
    snapshot: Snapshot,
) -> None:
    snapshot.snapshot_dir = "tests/cli/snapshots/transform"
    input_args, stdin = get_input_args(csv_file, input_mode)

    results = {}
    for test_name, args in TRANSFORM_COMMANDS.items():
        result = runner.invoke(app, [*args, *input_args, "--json"], input=stdin)
        assert result.exit_code == 0, f"{test_name} failed: {result.stdout}"
        results[test_name] = json.loads(result.stdout)

    snapshot.assert_match(json.dumps(results, indent=2), f"transform_{csv_file.stem}.json")


MERGE_COMMANDS = {
    "merge_on_single_inner": ["--on", "id", "--how", "inner"],
    "merge_on_single_outer": ["--on", "id", "--how", "outer"],
    "merge_on_multiple_inner": ["--on", "id,dept", "--how", "inner"],
    "merge_on_multiple_outer": ["--on", "id,dept", "--how", "outer"],
    "merge_left_on_right_on": ["--left-on", "id", "--right-on", "id", "--how", "inner"],
}


def test_merge_commands(tmp_path: Path, snapshot: Snapshot) -> None:
    """Test merge commands - requires two files with join keys."""
    snapshot.snapshot_dir = "tests/cli/snapshots/transform"

    left_df = pd.DataFrame(
        {"id": [1, 2, 3], "dept": ["Eng", "Sales", "Eng"], "name": ["Alice", "Bob", "Charlie"]}
    )
    right_df = pd.DataFrame(
        {"id": [1, 2, 3], "dept": ["Eng", "Sales", "HR"], "budget": [100000, 80000, 90000]}
    )

    left_file = tmp_path / "left.csv"
    right_file = tmp_path / "right.csv"
    left_df.to_csv(left_file, index=False)
    right_df.to_csv(right_file, index=False)

    results = {}
    for test_name, command in MERGE_COMMANDS.items():
        result = runner.invoke(app, ["merge", str(left_file), str(right_file), *command, "--json"])
        assert result.exit_code == 0, f"{test_name} failed: {result.stdout}"
        results[test_name] = json.loads(result.stdout)

    snapshot.assert_match(json.dumps(results, indent=2), "merge_commands.json")


def test_batch_command(tmp_path: Path, sample_csv_file: Path, snapshot: Snapshot) -> None:
    """Test batch command - creates multiple output files."""
    snapshot.snapshot_dir = "tests/cli/snapshots/transform"

    output_pattern = str(tmp_path / "batch_{}.json")
    result = runner.invoke(
        app, ["batch", str(sample_csv_file), "--sizes", "2", "-o", output_pattern]
    )

    batch_files = []
    for i in range(3):
        batch_file = tmp_path / f"batch_{i}.json"
        if batch_file.exists():
            batch_files.append(
                {"filename": f"batch_{i}.json", "content": json.loads(batch_file.read_text())}
            )

    normalized_stdout = result.stdout.replace(str(tmp_path), "<TMP>").replace("\\", "/")

    results = {
        "exit_code": result.exit_code,
        "stdout": normalized_stdout,
        "batch_files": batch_files,
    }
    snapshot.assert_match(json.dumps(results, indent=2), "batch_commands.json")


def test_concat_command(tmp_path: Path, sample_df: pd.DataFrame, snapshot: Snapshot) -> None:
    """Test concat command - combines multiple files."""
    snapshot.snapshot_dir = "tests/cli/snapshots/transform"

    file1 = tmp_path / "part1.csv"
    file2 = tmp_path / "part2.csv"
    file3 = tmp_path / "part3.csv"
    sample_df.head(2).to_csv(file1, index=False)
    sample_df.iloc[2:4].to_csv(file2, index=False)
    sample_df.tail(1).to_csv(file3, index=False)

    results = {}

    result = runner.invoke(app, ["concat", str(file1), str(file2), "--json"])
    assert result.exit_code == 0, f"concat_two failed: {result.stdout}"
    results["concat_two"] = json.loads(result.stdout)

    result = runner.invoke(app, ["concat", str(file1), str(file2), str(file3), "--json"])
    assert result.exit_code == 0, f"concat_three failed: {result.stdout}"
    results["concat_three"] = json.loads(result.stdout)

    snapshot.assert_match(json.dumps(results, indent=2), "concat_commands.json")


def test_concat_glob(tmp_path: Path, snapshot: Snapshot) -> None:
    """Test concat command with glob pattern."""
    snapshot.snapshot_dir = "tests/cli/snapshots/transform"

    (tmp_path / "data_001.csv").write_text("name,age\nAlice,25\n")
    (tmp_path / "data_002.csv").write_text("name,age\nBob,30\n")
    (tmp_path / "data_003.csv").write_text("name,age\nCharlie,35\n")

    glob_pattern = str(tmp_path / "data_*.csv")
    result = runner.invoke(app, ["concat", glob_pattern, "--json"])
    assert result.exit_code == 0, f"concat_glob failed: {result.stdout}"

    results = {"concat_glob": json.loads(result.stdout)}
    snapshot.assert_match(json.dumps(results, indent=2), "concat_glob_commands.json")
