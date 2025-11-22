"""Tests for filter_service module."""

import pandas as pd

from src.core import filter_service


def test_filter_by_query(sample_df: pd.DataFrame) -> None:
    """Test filtering with query expression."""
    result = filter_service.filter_by_query(sample_df, "age > 30")
    assert len(result) == 3
    assert all(result["age"] > 30)


def test_filter_by_query_multiple_conditions(sample_df: pd.DataFrame) -> None:
    """Test filtering with multiple conditions."""
    result = filter_service.filter_by_query(sample_df, "age > 30 and city == 'NYC'")
    assert len(result) == 1
    assert result.iloc[0]["name"] == "David"


def test_filter_by_value(sample_df: pd.DataFrame) -> None:
    """Test filtering by specific value."""
    result = filter_service.filter_by_value(sample_df, "city", "NYC")
    assert len(result) == 2
    assert all(result["city"] == "NYC")


def test_filter_null_remove_nulls(sample_df_with_nulls: pd.DataFrame) -> None:
    """Test removing rows with null values."""
    result = filter_service.filter_null(sample_df_with_nulls, "name", keep_null=False)
    assert len(result) == 4
    assert result["name"].notna().all()


def test_filter_null_keep_nulls(sample_df_with_nulls: pd.DataFrame) -> None:
    """Test keeping only rows with null values."""
    result = filter_service.filter_null(sample_df_with_nulls, "name", keep_null=True)
    assert len(result) == 1
    assert result["name"].isna().all()


def test_head_default(sample_df: pd.DataFrame) -> None:
    """Test head with default value."""
    result = filter_service.head(sample_df, 3)
    assert len(result) == 3
    assert result.iloc[0]["name"] == "Alice"


def test_head_more_than_length(sample_df: pd.DataFrame) -> None:
    """Test head with n greater than dataframe length."""
    result = filter_service.head(sample_df, 100)
    assert len(result) == 5


def test_tail_default(sample_df: pd.DataFrame) -> None:
    """Test tail with default value."""
    result = filter_service.tail(sample_df, 3)
    assert len(result) == 3
    assert result.iloc[-1]["name"] == "Eve"


def test_tail_more_than_length(sample_df: pd.DataFrame) -> None:
    """Test tail with n greater than dataframe length."""
    result = filter_service.tail(sample_df, 100)
    assert len(result) == 5


def test_sample_by_n(sample_df: pd.DataFrame) -> None:
    """Test sampling by number of rows."""
    result = filter_service.sample(sample_df, n=3, seed=42)
    assert len(result) == 3


def test_sample_by_frac(sample_df: pd.DataFrame) -> None:
    """Test sampling by fraction."""
    result = filter_service.sample(sample_df, frac=0.6, seed=42)
    assert len(result) == 3


def test_sample_reproducible(sample_df: pd.DataFrame) -> None:
    """Test that sampling with same seed produces same results."""
    result1 = filter_service.sample(sample_df, n=3, seed=42)
    result2 = filter_service.sample(sample_df, n=3, seed=42)
    pd.testing.assert_frame_equal(result1, result2)
