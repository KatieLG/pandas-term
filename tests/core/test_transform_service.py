"""Tests for transform_service module."""

import pandas as pd
import pytest

from src.core import transform_service


def test_select_columns(sample_df: pd.DataFrame) -> None:
    """Test selecting specific columns."""
    result = transform_service.select_columns(sample_df, ["name", "age"])
    assert list(result.columns) == ["name", "age"]
    assert len(result) == 5


def test_select_columns_missing(sample_df: pd.DataFrame) -> None:
    """Test selecting columns that don't exist."""
    with pytest.raises(ValueError, match="Columns not found"):
        transform_service.select_columns(sample_df, ["name", "nonexistent"])


def test_drop_columns(sample_df: pd.DataFrame) -> None:
    """Test dropping specific columns."""
    result = transform_service.drop_columns(sample_df, ["age", "salary"])
    assert "age" not in result.columns
    assert "salary" not in result.columns
    assert "name" in result.columns


def test_drop_columns_nonexistent(sample_df: pd.DataFrame) -> None:
    """Test dropping columns that don't exist."""
    result = transform_service.drop_columns(sample_df, ["nonexistent"])
    assert len(result.columns) == len(sample_df.columns)


def test_rename_columns(sample_df: pd.DataFrame) -> None:
    """Test renaming columns."""
    result = transform_service.rename_columns(sample_df, {"name": "full_name", "age": "years"})
    assert "full_name" in result.columns
    assert "years" in result.columns
    assert "name" not in result.columns


def test_sort_by_ascending(sample_df: pd.DataFrame) -> None:
    """Test sorting in ascending order."""
    result = transform_service.sort_by(sample_df, ["age"], ascending=True)
    assert result.iloc[0]["age"] == 25
    assert result.iloc[-1]["age"] == 45


def test_sort_by_descending(sample_df: pd.DataFrame) -> None:
    """Test sorting in descending order."""
    result = transform_service.sort_by(sample_df, ["age"], ascending=False)
    assert result.iloc[0]["age"] == 45
    assert result.iloc[-1]["age"] == 25


def test_drop_duplicates(sample_df: pd.DataFrame) -> None:
    """Test dropping duplicate rows."""
    df_with_dups = sample_df.copy()
    df_with_dups = pd.concat([df_with_dups, sample_df.iloc[[0]]], ignore_index=True)

    result = transform_service.drop_duplicates(df_with_dups)
    assert len(result) == 5


def test_reset_index(sample_df: pd.DataFrame) -> None:
    """Test resetting the index."""
    df = sample_df.copy()
    df = df[df["age"] > 30]
    result = transform_service.reset_index(df)

    assert result.index[0] == 0
    assert list(result.index) == list(range(len(result)))
