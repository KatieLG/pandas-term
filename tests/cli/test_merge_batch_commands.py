"""Tests for merge and batch CLI commands."""

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from src.main import app

runner = CliRunner()


def test_merge_command(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    """Test merge command."""
    left_file = tmp_path / "left.csv"
    right_file = tmp_path / "right.csv"

    left_df = sample_df[["name", "age"]].copy()
    right_df = sample_df[["name", "salary"]].copy()

    left_df.to_csv(left_file, index=False)
    right_df.to_csv(right_file, index=False)

    result = runner.invoke(app, ["merge", str(left_file), str(right_file), "--on", "name"])
    assert result.exit_code == 0
    assert "Alice" in result.stdout
    assert "age" in result.stdout
    assert "salary" in result.stdout


def test_merge_with_different_columns(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    """Test merge command with different column names."""
    left_file = tmp_path / "left.csv"
    right_file = tmp_path / "right.csv"

    left_df = sample_df[["name", "age"]].copy()
    right_df = sample_df[["name", "salary"]].copy()
    right_df = right_df.rename(columns={"name": "person"})

    left_df.to_csv(left_file, index=False)
    right_df.to_csv(right_file, index=False)

    result = runner.invoke(
        app, ["merge", str(left_file), str(right_file), "--left-on", "name", "--right-on", "person"]
    )
    assert result.exit_code == 0


def test_merge_outer(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    """Test merge command with outer join."""
    left_file = tmp_path / "left.csv"
    right_file = tmp_path / "right.csv"

    left_df = sample_df[["name", "age"]].head(3)
    right_df = sample_df[["name", "salary"]].tail(3)

    left_df.to_csv(left_file, index=False)
    right_df.to_csv(right_file, index=False)

    result = runner.invoke(
        app, ["merge", str(left_file), str(right_file), "--on", "name", "--how", "outer"]
    )
    assert result.exit_code == 0


def test_batch_command(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    """Test batch command."""
    input_file = tmp_path / "input.csv"
    sample_df.to_csv(input_file, index=False)

    result = runner.invoke(
        app, ["batch", str(input_file), "2", "-o", str(tmp_path / "batch_{}.csv")]
    )
    assert result.exit_code == 0
    assert "batch 0" in result.stdout
    assert "batch 1" in result.stdout
    assert "batch 2" in result.stdout

    assert (tmp_path / "batch_0.csv").exists()
    assert (tmp_path / "batch_1.csv").exists()
    assert (tmp_path / "batch_2.csv").exists()

    batch_0 = pd.read_csv(tmp_path / "batch_0.csv")
    assert len(batch_0) == 2


def test_batch_exact_division(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    """Test batch command with exact division."""
    input_file = tmp_path / "input.csv"
    df = sample_df.head(4)
    df.to_csv(input_file, index=False)

    result = runner.invoke(
        app, ["batch", str(input_file), "2", "-o", str(tmp_path / "chunk_{}.csv")]
    )
    assert result.exit_code == 0

    assert (tmp_path / "chunk_0.csv").exists()
    assert (tmp_path / "chunk_1.csv").exists()
    assert not (tmp_path / "chunk_2.csv").exists()
