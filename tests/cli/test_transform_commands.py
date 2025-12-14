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
    "select_multiple": ["select", "name,price,category"],
    "drop_single": ["drop", "stock"],
    "drop_multiple": ["drop", "category,stock"],
    "sort_single_asc": ["sort", "price", "--ascending"],
    "sort_single_desc": ["sort", "price", "--descending"],
    "sort_multiple_asc": ["sort", "category,price", "--ascending"],
    "sort_multiple_desc": ["sort", "category,price", "--descending"],
    "rename_single": ["rename", "name:product_name"],
    "rename_multiple": ["rename", "name:product_name,price:cost"],
    "dedup_all": ["dedup"],
    "dedup_subset_single": ["dedup", "--subset", "name"],
    "dedup_subset_multiple": ["dedup", "--subset", "name,price"],
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
    "merge_on_single_left": ["--on", "id", "--how", "left"],
    "merge_on_single_right": ["--on", "id", "--how", "right"],
    "merge_on_single_outer": ["--on", "id", "--how", "outer"],
    "merge_on_multiple_inner": ["--on", "id,aisle", "--how", "inner"],
    "merge_on_multiple_outer": ["--on", "id,aisle", "--how", "outer"],
}


def test_merge_commands(tmp_path: Path, snapshot: Snapshot) -> None:
    """Test merging - requires explicit files"""
    snapshot.snapshot_dir = "tests/cli/snapshots/transform"

    left_df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "aisle": ["Produce", "Dairy", "Produce"],
            "name": ["Apple", "Cheese", "Banana"],
        }
    )
    right_df = pd.DataFrame(
        {
            "id": [2, 3, 4],
            "aisle": ["Dairy", "Bakery", "Produce"],
            "stock": [30, 50, 75],
        }
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
    snapshot.snapshot_dir = "tests/cli/snapshots/transform"

    output_pattern = str(tmp_path / "batch_{}.json")
    result = runner.invoke(
        app, ["batch", str(sample_csv_file), "--sizes", "2", "-o", output_pattern]
    )

    assert result.exit_code == 0
    batch_files = sorted(tmp_path.rglob("batch_*.json"))
    assert len(batch_files) == 3

    batch_data = [{"filename": f.name, "content": json.loads(f.read_text())} for f in batch_files]
    snapshot.assert_match(json.dumps(batch_data, indent=2), "batch_commands.json")


def test_concat_command(tmp_path: Path, sample_df: pd.DataFrame, snapshot: Snapshot) -> None:
    """Split df into segments and test concat with explicit names & glob work"""
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

    result = runner.invoke(app, ["concat", f"{tmp_path}/*1.csv", "--json"])
    assert result.exit_code == 0, f"concat_one_glob failed: {result.stdout}"
    results["concat_one_glob"] = json.loads(result.stdout)

    result = runner.invoke(app, ["concat", f"{tmp_path}/*.csv", "--json"])
    assert result.exit_code == 0, f"concat_all_glob failed: {result.stdout}"
    results["concat_all_glob"] = json.loads(result.stdout)

    snapshot.assert_match(json.dumps(results, indent=2), "concat_commands.json")
