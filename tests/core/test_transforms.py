"""Tests for transforms module."""

import pandas as pd

from pandas_cli.core import transforms


def test_batch_dataframe_single_size(sample_df: pd.DataFrame) -> None:
    """Test splitting dataframe into batches with single size."""
    batches = transforms.batch_dataframe(sample_df, sizes=[2])
    assert len(batches) == 3
    assert len(batches[0]) == 2
    assert len(batches[1]) == 2
    assert len(batches[2]) == 1


def test_batch_dataframe_variable_sizes(sample_df: pd.DataFrame) -> None:
    """Test batching with variable sizes that repeat last size."""
    batches = transforms.batch_dataframe(sample_df, sizes=[1, 2])
    # 5 rows: 1, 2, 2 (last size repeats)
    assert len(batches) == 3
    assert len(batches[0]) == 1
    assert len(batches[1]) == 2
    assert len(batches[2]) == 2


def test_batch_dataframe_exact_division(sample_df: pd.DataFrame) -> None:
    """Test batching when size divides evenly."""
    df = sample_df.head(4)
    batches = transforms.batch_dataframe(df, sizes=[2])
    assert len(batches) == 2
    assert len(batches[0]) == 2
    assert len(batches[1]) == 2
