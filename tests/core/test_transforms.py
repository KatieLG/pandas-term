"""Tests for transforms module."""

import pandas as pd
import pytest

from pandas_cli.core import transforms


def test_validate_columns_valid(sample_df: pd.DataFrame) -> None:
    """Test validating columns that exist."""
    transforms.validate_columns(sample_df, ["name", "age"])


def test_validate_columns_missing(sample_df: pd.DataFrame) -> None:
    """Test validating columns that don't exist."""
    with pytest.raises(ValueError, match="Columns not found"):
        transforms.validate_columns(sample_df, ["name", "nonexistent"])


def test_batch_dataframe(sample_df: pd.DataFrame) -> None:
    """Test splitting dataframe into batches."""
    batches = transforms.batch_dataframe(sample_df, batch_size=2)
    assert len(batches) == 3
    assert len(batches[0]) == 2
    assert len(batches[1]) == 2
    assert len(batches[2]) == 1


def test_batch_dataframe_exact_division(sample_df: pd.DataFrame) -> None:
    """Test batching when size divides evenly."""
    df = sample_df.head(4)
    batches = transforms.batch_dataframe(df, batch_size=2)
    assert len(batches) == 2
    assert len(batches[0]) == 2
    assert len(batches[1]) == 2
