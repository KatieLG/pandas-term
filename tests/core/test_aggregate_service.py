"""Tests for aggregate_service module."""

import pandas as pd

from pandas_cli.core import aggregate_service


def test_value_counts(sample_df: pd.DataFrame) -> None:
    """Test value counts for a column."""
    result = aggregate_service.value_counts(sample_df, "city")
    assert len(result) == 3
    assert "NYC" in result["city"].to_numpy()


def test_value_counts_normalize(sample_df: pd.DataFrame) -> None:
    """Test normalized value counts."""
    result = aggregate_service.value_counts(sample_df, "department", normalize=True)
    assert len(result) == 2
    total = result["proportion"].sum()
    assert abs(total - 1.0) < 0.01


def test_group_by_sum(sample_df: pd.DataFrame) -> None:
    """Test groupby with sum aggregation."""
    result = aggregate_service.group_by(sample_df, ["department"], "salary", "sum")
    assert len(result) == 2
    assert "department" in result.columns
    assert "salary" in result.columns


def test_group_by_mean(sample_df: pd.DataFrame) -> None:
    """Test groupby with mean aggregation."""
    result = aggregate_service.group_by(sample_df, ["city"], "age", "mean")
    assert len(result) == 3
    assert "city" in result.columns


def test_group_by_count(sample_df: pd.DataFrame) -> None:
    """Test groupby with count aggregation."""
    result = aggregate_service.group_by(sample_df, ["city"], "name", "count")
    assert len(result) == 3
    nyc_count = result[result["city"] == "NYC"]["name"].iloc[0]
    assert nyc_count == 2
