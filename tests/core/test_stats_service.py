"""Tests for stats_service module."""

import pandas as pd

from pandas_cli.core import stats_service


def test_describe(sample_df: pd.DataFrame) -> None:
    """Test descriptive statistics generation."""
    result = stats_service.describe(sample_df)
    assert "age" in result.columns
    assert "salary" in result.columns
    assert "mean" in result.index


def test_info(sample_df: pd.DataFrame) -> None:
    """Test dataframe info generation."""
    result = stats_service.info(sample_df)
    assert isinstance(result, str)
    assert "DataFrame" in result
    assert "entries" in result


def test_unique_values(sample_df: pd.DataFrame) -> None:
    """Test getting unique values from a column."""
    result = stats_service.unique_values(sample_df, "city")
    assert len(result) == 3
    assert set(result) == {"NYC", "LA", "Chicago"}


def test_size(sample_df: pd.DataFrame) -> None:
    """Test getting total number of elements."""
    result = stats_service.size(sample_df)
    assert result == 25  # 5 rows x 5 columns


def test_shape(sample_df: pd.DataFrame) -> None:
    """Test getting dimensions."""
    result = stats_service.shape(sample_df)
    assert result == (5, 5)


def test_columns(sample_df: pd.DataFrame) -> None:
    """Test getting column names."""
    result = stats_service.columns(sample_df)
    assert "name" in result
    assert "age" in result
    assert "city" in result
    assert len(result) == 5


def test_memory_usage(sample_df: pd.DataFrame) -> None:
    """Test getting memory usage."""
    result = stats_service.memory_usage(sample_df)
    assert len(result) > 0
    assert result.sum() > 0


def test_memory_usage_deep(sample_df: pd.DataFrame) -> None:
    """Test getting deep memory usage."""
    result = stats_service.memory_usage(sample_df, deep=True)
    assert len(result) > 0
    assert result.sum() > 0
