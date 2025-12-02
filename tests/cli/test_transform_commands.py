"""Snapshot tests for transform CLI commands."""

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
    """Standard test dataset for transform command tests."""
    return pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [25, 30, 35, 40, 45],
            "city": ["NYC", "LA", "Chicago", "NYC", "LA"],
            "salary": [50000, 60000, 70000, 80000, 90000],
        }
    )


@pytest.fixture
def test_data_with_duplicates() -> pd.DataFrame:
    """Test dataset with duplicate rows."""
    return pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Alice", "Charlie", "Alice"],
            "age": [30, 25, 30, 35, 31],
            "city": ["NYC", "LA", "NYC", "NYC", "NYC"],
        }
    )


@pytest.fixture
def left_data() -> pd.DataFrame:
    """Left dataframe for merge tests."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "dept": ["Eng", "Sales", "Eng"],
            "name": ["Alice", "Bob", "Charlie"],
        }
    )


@pytest.fixture
def right_data() -> pd.DataFrame:
    """Right dataframe for merge tests."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "dept": ["Eng", "Sales", "HR"],
            "budget": [100000, 80000, 90000],
        }
    )


TRANSFORM_COMMANDS = {
    "select_single": ["select", "name"],
    "select_multiple": ["select", "name,age,city"],
    "drop_single": ["drop", "salary"],
    "drop_multiple": ["drop", "city,salary"],
    "sort_single_asc": ["sort", "age", "--ascending"],
    "sort_single_desc": ["sort", "age", "--descending"],
    "sort_multiple_asc": ["sort", "city,age", "--ascending"],
    "sort_multiple_desc": ["sort", "city,age", "--descending"],
}


DEDUP_COMMANDS = {
    "dedup_all": ["dedup"],
    "dedup_subset_single": ["dedup", "--subset", "name"],
    "dedup_subset_multiple": ["dedup", "--subset", "name,age"],
}


MERGE_COMMANDS = {
    "merge_on_single_inner": ["--on", "id", "--how", "inner"],
    "merge_on_single_outer": ["--on", "id", "--how", "outer"],
    "merge_on_multiple_inner": ["--on", "id,dept", "--how", "inner"],
    "merge_on_multiple_outer": ["--on", "id,dept", "--how", "outer"],
    "merge_left_on_right_on": ["--left-on", "id", "--right-on", "id", "--how", "inner"],
}


def test_transform_commands(tmp_path: Path, test_data: pd.DataFrame, snapshot: Snapshot) -> None:
    """Test all basic transform commands against snapshots."""
    snapshot.snapshot_dir = "tests/cli/snapshots/transform"

    csv_file = tmp_path / "test.csv"
    test_data.to_csv(csv_file, index=False)

    results = {}
    for test_name, command in TRANSFORM_COMMANDS.items():
        result = runner.invoke(app, command + [str(csv_file)])
        results[test_name] = {
            "exit_code": result.exit_code,
            "stdout": result.stdout,
            "stderr": result.stderr if result.stderr else None,
        }

    snapshot.assert_match(
        json.dumps(results, indent=4, ensure_ascii=False), "transform_commands.json"
    )


def test_dedup_commands(
    tmp_path: Path, test_data_with_duplicates: pd.DataFrame, snapshot: Snapshot
) -> None:
    """Test dedup commands against snapshots."""
    snapshot.snapshot_dir = "tests/cli/snapshots/transform"

    csv_file = tmp_path / "test_dups.csv"
    test_data_with_duplicates.to_csv(csv_file, index=False)

    results = {}
    for test_name, command in DEDUP_COMMANDS.items():
        result = runner.invoke(app, command + [str(csv_file)])
        results[test_name] = {
            "exit_code": result.exit_code,
            "stdout": result.stdout,
            "stderr": result.stderr if result.stderr else None,
        }

    snapshot.assert_match(json.dumps(results, indent=4, ensure_ascii=False), "dedup_commands.json")


def test_merge_commands(
    tmp_path: Path, left_data: pd.DataFrame, right_data: pd.DataFrame, snapshot: Snapshot
) -> None:
    """Test merge commands against snapshots."""
    snapshot.snapshot_dir = "tests/cli/snapshots/transform"

    left_file = tmp_path / "left.csv"
    right_file = tmp_path / "right.csv"
    left_data.to_csv(left_file, index=False)
    right_data.to_csv(right_file, index=False)

    results = {}
    for test_name, command in MERGE_COMMANDS.items():
        result = runner.invoke(app, ["merge", str(left_file), str(right_file)] + command)
        results[test_name] = {
            "exit_code": result.exit_code,
            "stdout": result.stdout,
            "stderr": result.stderr if result.stderr else None,
        }

    snapshot.assert_match(json.dumps(results, indent=4, ensure_ascii=False), "merge_commands.json")


def test_batch_command(tmp_path: Path, test_data: pd.DataFrame, snapshot: Snapshot) -> None:
    """Test batch command against snapshots."""
    snapshot.snapshot_dir = "tests/cli/snapshots/transform"

    csv_file = tmp_path / "test.csv"
    test_data.to_csv(csv_file, index=False)

    output_pattern = str(tmp_path / "batch_{}.csv")
    result = runner.invoke(app, ["batch", "2", str(csv_file), "-o", output_pattern])

    batch_files = []
    for i in range(3):
        batch_file = tmp_path / f"batch_{i}.csv"
        if batch_file.exists():
            batch_files.append(
                {
                    "filename": f"batch_{i}.csv",
                    "content": batch_file.read_text(),
                }
            )

    # Normalize paths in stdout by replacing tmp_path with <TMP>
    normalized_stdout = result.stdout.replace(str(tmp_path), "<TMP>")

    results = {
        "exit_code": result.exit_code,
        "stdout": normalized_stdout,
        "stderr": result.stderr if result.stderr else None,
        "batch_files": batch_files,
    }

    snapshot.assert_match(json.dumps(results, indent=4, ensure_ascii=False), "batch_commands.json")
