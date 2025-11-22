"""Tests for filter CLI commands."""

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from src.main import app

runner = CliRunner()


def test_query_command(sample_csv_file: Path) -> None:
    """Test query command."""
    result = runner.invoke(app, ["query", str(sample_csv_file), "age > 30"])
    assert result.exit_code == 0
    assert "Charlie" in result.stdout
    assert "Alice" not in result.stdout


def test_query_command_multiple_conditions(sample_csv_file: Path) -> None:
    """Test query command with multiple conditions."""
    result = runner.invoke(app, ["query", str(sample_csv_file), "age > 30 and city == 'NYC'"])
    assert result.exit_code == 0
    assert "David" in result.stdout


def test_head_command_default(sample_csv_file: Path) -> None:
    """Test head command with default value."""
    result = runner.invoke(app, ["head", str(sample_csv_file)])
    assert result.exit_code == 0
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 6


def test_head_command_custom_n(sample_csv_file: Path) -> None:
    """Test head command with custom n value."""
    result = runner.invoke(app, ["head", str(sample_csv_file), "--n", "3"])
    assert result.exit_code == 0
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 4


def test_tail_command_default(sample_csv_file: Path) -> None:
    """Test tail command with default value."""
    result = runner.invoke(app, ["tail", str(sample_csv_file)])
    assert result.exit_code == 0
    assert "Eve" in result.stdout


def test_tail_command_custom_n(sample_csv_file: Path) -> None:
    """Test tail command with custom n value."""
    result = runner.invoke(app, ["tail", str(sample_csv_file), "--n", "2"])
    assert result.exit_code == 0
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 3


def test_sample_command_by_n(sample_csv_file: Path) -> None:
    """Test sample command with n parameter."""
    result = runner.invoke(app, ["sample", str(sample_csv_file), "--n", "3", "--seed", "42"])
    assert result.exit_code == 0
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 4


def test_sample_command_by_frac(sample_csv_file: Path) -> None:
    """Test sample command with frac parameter."""
    result = runner.invoke(app, ["sample", str(sample_csv_file), "--frac", "0.6", "--seed", "42"])
    assert result.exit_code == 0
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 4


def test_dropna_command(tmp_path: Path, sample_df_with_nulls: pd.DataFrame) -> None:
    """Test dropna command."""
    csv_file = tmp_path / "test_with_nulls.csv"
    sample_df_with_nulls.to_csv(csv_file, index=False)

    result = runner.invoke(app, ["dropna", str(csv_file), "name"])
    assert result.exit_code == 0
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 5


def test_query_with_output_file(sample_csv_file: Path, tmp_path: Path) -> None:
    """Test query command with output file."""
    output_file = tmp_path / "output.csv"
    result = runner.invoke(app, ["query", str(sample_csv_file), "age > 30", "-o", str(output_file)])
    assert result.exit_code == 0
    assert output_file.exists()

    df = pd.read_csv(output_file)
    assert len(df) == 3
    assert all(df["age"] > 30)
