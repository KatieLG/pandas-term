"""Tests for stats CLI commands."""

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from src.main import app

runner = CliRunner()


def test_describe_command(sample_csv_file: Path) -> None:
    """Test describe command."""
    result = runner.invoke(app, ["describe", str(sample_csv_file)])
    assert result.exit_code == 0
    assert "age" in result.stdout
    assert "salary" in result.stdout


def test_info_command(sample_csv_file: Path) -> None:
    """Test info command."""
    result = runner.invoke(app, ["info", str(sample_csv_file)])
    assert result.exit_code == 0
    assert "DataFrame" in result.stdout or "entries" in result.stdout


def test_value_counts_command(sample_csv_file: Path) -> None:
    """Test value_counts command."""
    result = runner.invoke(app, ["value-counts", str(sample_csv_file), "city"])
    assert result.exit_code == 0
    assert "NYC" in result.stdout
    assert "LA" in result.stdout


def test_value_counts_normalized(sample_csv_file: Path) -> None:
    """Test value_counts command with normalization."""
    result = runner.invoke(app, ["value-counts", str(sample_csv_file), "city", "--normalize"])
    assert result.exit_code == 0
    assert "0." in result.stdout


def test_groupby_command(sample_csv_file: Path) -> None:
    """Test groupby command."""
    result = runner.invoke(
        app,
        [
            "groupby",
            str(sample_csv_file),
            "department",
            "--agg-column",
            "salary",
            "--agg-func",
            "sum",
        ],
    )
    assert result.exit_code == 0
    assert "Engineering" in result.stdout
    assert "Sales" in result.stdout


def test_groupby_with_mean(sample_csv_file: Path) -> None:
    """Test groupby command with mean aggregation."""
    result = runner.invoke(
        app, ["groupby", str(sample_csv_file), "city", "--agg-column", "age", "--agg-func", "mean"]
    )
    assert result.exit_code == 0
    assert "NYC" in result.stdout


def test_corr_command(sample_csv_file: Path) -> None:
    """Test correlation command."""
    result = runner.invoke(app, ["corr", str(sample_csv_file)])
    assert result.exit_code == 0
    assert "age" in result.stdout
    assert "salary" in result.stdout


def test_corr_specific_columns(sample_csv_file: Path) -> None:
    """Test correlation command with specific columns."""
    result = runner.invoke(
        app, ["corr", str(sample_csv_file), "--columns", "age", "--columns", "salary"]
    )
    assert result.exit_code == 0


def test_missing_command_no_nulls(sample_csv_file: Path) -> None:
    """Test missing command with no null values."""
    result = runner.invoke(app, ["missing", str(sample_csv_file)])
    assert result.exit_code == 0


def test_missing_command_with_nulls(tmp_path: Path, sample_df_with_nulls: pd.DataFrame) -> None:
    """Test missing command with null values."""
    csv_file = tmp_path / "test_with_nulls.csv"
    sample_df_with_nulls.to_csv(csv_file, index=False)

    result = runner.invoke(app, ["missing", str(csv_file)])
    assert result.exit_code == 0
    assert "missing_count" in result.stdout or "name" in result.stdout


def test_unique_command(sample_csv_file: Path) -> None:
    """Test unique command."""
    result = runner.invoke(app, ["unique", str(sample_csv_file), "city"])
    assert result.exit_code == 0
    assert "NYC" in result.stdout
    assert "LA" in result.stdout
    assert "Chicago" in result.stdout


def test_describe_with_output_file(sample_csv_file: Path, tmp_path: Path) -> None:
    """Test describe command with output file."""
    output_file = tmp_path / "output.csv"
    result = runner.invoke(app, ["describe", str(sample_csv_file), "-o", str(output_file)])
    assert result.exit_code == 0
    assert output_file.exists()

    df = pd.read_csv(output_file)
    assert "age" in df.columns
