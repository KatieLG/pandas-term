"""Tests for stats CLI commands."""

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from pandas_cli.main import app

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
            "--col",
            "salary",
            "--agg",
            "sum",
        ],
    )
    assert result.exit_code == 0
    assert "Engineering" in result.stdout
    assert "Sales" in result.stdout


def test_groupby_with_mean(sample_csv_file: Path) -> None:
    """Test groupby command with mean aggregation."""
    result = runner.invoke(
        app, ["groupby", str(sample_csv_file), "city", "--col", "age", "--agg", "mean"]
    )
    assert result.exit_code == 0
    assert "NYC" in result.stdout


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
