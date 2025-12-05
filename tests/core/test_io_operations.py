"""Tests for io_operations module."""

from collections.abc import Callable
from pathlib import Path

import pandas as pd
import pytest

from pandas_term.cli.options import OutputOptions
from pandas_term.core import io_operations


@pytest.mark.parametrize(
    ("extension", "writer"),
    [
        (".csv", lambda df, p: df.to_csv(p, index=False)),
        (".tsv", lambda df, p: df.to_csv(p, index=False, sep="\t")),
        (".xlsx", lambda df, p: df.to_excel(p, index=False)),
        (".json", lambda df, p: df.to_json(p, orient="records", indent=2)),
        (".parquet", lambda df, p: df.to_parquet(p, index=False)),
    ],
)
def test_read_formats(
    tmp_path: Path,
    sample_df: pd.DataFrame,
    extension: str,
    writer: Callable[[pd.DataFrame, Path], None],
) -> None:
    """Test reading various file formats."""
    file_path = tmp_path / f"test{extension}"
    writer(sample_df, file_path)

    df = io_operations.read_dataframe(str(file_path))
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


@pytest.mark.parametrize(
    ("extension", "reader"),
    [
        (".csv", lambda p: pd.read_csv(p)),
        (".tsv", lambda p: pd.read_csv(p, sep="\t")),
        (".xlsx", lambda p: pd.read_excel(p)),
        (".json", lambda p: pd.read_json(p)),
        (".parquet", lambda p: pd.read_parquet(p)),
    ],
)
def test_write_formats(
    tmp_path: Path,
    sample_df: pd.DataFrame,
    extension: str,
    reader: Callable[[Path], pd.DataFrame],
) -> None:
    """Test writing various file formats."""
    output_path = tmp_path / f"output{extension}"
    io_operations.write_dataframe(sample_df, OutputOptions(file=str(output_path)))

    df = reader(output_path)
    assert len(df) == 5
    assert "name" in df.columns


def test_write_markdown(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    """Test writing a Markdown file."""
    output_path = tmp_path / "output.md"
    io_operations.write_dataframe(sample_df, OutputOptions(file=str(output_path)))

    content = output_path.read_text()
    assert "| name" in content
    assert "Alice" in content


def test_write_unsupported_format(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    """Test writing to an unsupported file format."""
    output_path = tmp_path / "output.txt"

    with pytest.raises(ValueError, match="Unsupported file format"):
        io_operations.write_dataframe(sample_df, OutputOptions(file=str(output_path)))
