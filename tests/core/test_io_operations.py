"""Tests for io_operations module."""

from pathlib import Path

import pandas as pd
import pytest

from pandas_term.cli.options import OutputOptions
from pandas_term.core import io_operations


def test_read_csv(sample_csv_file: Path) -> None:
    """Test reading a CSV file."""
    df = io_operations.read_dataframe(str(sample_csv_file))
    assert len(df) == 5
    assert list(df.columns) == ["name", "age", "city", "salary", "department"]


def test_read_excel(sample_excel_file: Path) -> None:
    """Test reading an Excel file."""
    df = io_operations.read_dataframe(str(sample_excel_file))
    assert len(df) == 5
    assert "name" in df.columns


def test_read_json(sample_json_file: Path) -> None:
    """Test reading a JSON file."""
    df = io_operations.read_dataframe(str(sample_json_file))
    assert len(df) == 5
    assert "name" in df.columns


def test_read_nonexistent_file() -> None:
    """Test reading a file that doesn't exist."""
    with pytest.raises(FileNotFoundError):
        io_operations.read_dataframe("/nonexistent/file.csv")


def test_read_unsupported_format(tmp_path: Path) -> None:
    """Test reading an unsupported file format."""
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("some text")

    with pytest.raises(ValueError, match="Unsupported file format"):
        io_operations.read_dataframe(str(txt_file))


def test_write_csv(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    """Test writing a CSV file."""
    output_path = tmp_path / "output.csv"
    io_operations.write_dataframe(sample_df, OutputOptions(file=str(output_path)))

    df = pd.read_csv(output_path)
    assert len(df) == 5
    assert list(df.columns) == ["name", "age", "city", "salary", "department"]


def test_write_excel(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    """Test writing an Excel file."""
    output_path = tmp_path / "output.xlsx"
    io_operations.write_dataframe(sample_df, OutputOptions(file=str(output_path)))

    df = pd.read_excel(output_path)
    assert len(df) == 5


def test_write_json(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    """Test writing a JSON file."""
    output_path = tmp_path / "output.json"
    io_operations.write_dataframe(sample_df, OutputOptions(file=str(output_path)))

    df = pd.read_json(output_path)
    assert len(df) == 5


def test_write_unsupported_format(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    """Test writing to an unsupported file format."""
    output_path = tmp_path / "output.txt"

    with pytest.raises(ValueError, match="Unsupported file format"):
        io_operations.write_dataframe(sample_df, OutputOptions(file=str(output_path)))
