"""Tests for transform CLI commands."""

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from pandas_cli.main import app

runner = CliRunner()


def test_select_command(sample_csv_file: Path) -> None:
    """Test select command."""
    result = runner.invoke(app, ["select", str(sample_csv_file), "name", "age"])
    assert result.exit_code == 0
    assert "name" in result.stdout
    assert "age" in result.stdout
    assert "salary" not in result.stdout


def test_drop_command(sample_csv_file: Path) -> None:
    """Test drop command."""
    result = runner.invoke(app, ["drop", str(sample_csv_file), "age", "salary"])
    assert result.exit_code == 0
    assert "name" in result.stdout
    assert "age" not in result.stdout
    assert "salary" not in result.stdout


def test_sort_command(sample_csv_file: Path) -> None:
    """Test sort command."""
    result = runner.invoke(app, ["sort", str(sample_csv_file), "age"])
    assert result.exit_code == 0
    lines = result.stdout.strip().split("\n")
    assert "25" in lines[1]


def test_sort_descending(sample_csv_file: Path) -> None:
    """Test sort command in descending order."""
    result = runner.invoke(app, ["sort", str(sample_csv_file), "age", "--descending"])
    assert result.exit_code == 0
    lines = result.stdout.strip().split("\n")
    assert "45" in lines[1]


def test_dedup_command(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    """Test dedup command."""
    csv_file = tmp_path / "test_with_dups.csv"
    df_with_dups = sample_df.copy()
    df_with_dups = pd.concat([df_with_dups, sample_df.iloc[[0]]], ignore_index=True)
    df_with_dups.to_csv(csv_file, index=False)

    result = runner.invoke(app, ["dedup", str(csv_file)])
    assert result.exit_code == 0
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 6


def test_reset_index_command(sample_csv_file: Path) -> None:
    """Test reset_index command."""
    result = runner.invoke(app, ["reset-index", str(sample_csv_file)])
    assert result.exit_code == 0


def test_select_with_output_file(sample_csv_file: Path, tmp_path: Path) -> None:
    """Test select command with output file."""
    output_file = tmp_path / "output.csv"
    result = runner.invoke(
        app, ["select", str(sample_csv_file), "name", "age", "-o", str(output_file)]
    )
    assert result.exit_code == 0
    assert output_file.exists()

    df = pd.read_csv(output_file)
    assert list(df.columns) == ["name", "age"]
