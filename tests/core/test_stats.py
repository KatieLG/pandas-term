"""Tests for stats module."""

import pandas as pd

from pandas_cli.core import stats


def test_describe(sample_df: pd.DataFrame) -> None:
    """Test descriptive statistics generation."""
    result = stats.describe(sample_df)
    assert "age" in result.columns
    assert "salary" in result.columns
    assert "mean" in result.index


def test_unique_values(sample_df: pd.DataFrame) -> None:
    """Test getting unique values from a column."""
    result = stats.unique_values(sample_df, "city")
    assert len(result) == 3
    assert set(result) == {"NYC", "LA", "Chicago"}


def test_shape(sample_df: pd.DataFrame) -> None:
    """Test getting dimensions."""
    result = stats.shape(sample_df)
    assert result == (5, 5)


def test_columns(sample_df: pd.DataFrame) -> None:
    """Test getting column names."""
    result = stats.columns(sample_df)
    assert "name" in result
    assert "age" in result
    assert "city" in result
    assert len(result) == 5
