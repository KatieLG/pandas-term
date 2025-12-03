"""Tests for transforms module."""

import pandas as pd
import pytest

from pandas_cli.core import transforms


def test_select_columns(sample_df: pd.DataFrame) -> None:
    """Test selecting specific columns."""
    result = transforms.select_columns(sample_df, ["name", "age"])
    assert list(result.columns) == ["name", "age"]
    assert len(result) == 5


def test_select_columns_missing(sample_df: pd.DataFrame) -> None:
    """Test selecting columns that don't exist."""
    with pytest.raises(ValueError, match="Columns not found"):
        transforms.select_columns(sample_df, ["name", "nonexistent"])


def test_drop_columns(sample_df: pd.DataFrame) -> None:
    """Test dropping specific columns."""
    result = transforms.drop_columns(sample_df, ["age", "salary"])
    assert "age" not in result.columns
    assert "salary" not in result.columns
    assert "name" in result.columns


def test_drop_columns_nonexistent(sample_df: pd.DataFrame) -> None:
    """Test dropping columns that don't exist."""
    result = transforms.drop_columns(sample_df, ["nonexistent"])
    assert len(result.columns) == len(sample_df.columns)


def test_rename_columns(sample_df: pd.DataFrame) -> None:
    """Test renaming columns."""
    result = transforms.rename_columns(sample_df, {"name": "full_name", "age": "years"})
    assert "full_name" in result.columns
    assert "years" in result.columns
    assert "name" not in result.columns


def test_sort_by_ascending(sample_df: pd.DataFrame) -> None:
    """Test sorting in ascending order."""
    result = transforms.sort_by(sample_df, ["age"], ascending=True)
    assert result.iloc[0]["age"] == 25
    assert result.iloc[-1]["age"] == 45


def test_sort_by_descending(sample_df: pd.DataFrame) -> None:
    """Test sorting in descending order."""
    result = transforms.sort_by(sample_df, ["age"], ascending=False)
    assert result.iloc[0]["age"] == 45
    assert result.iloc[-1]["age"] == 25


def test_drop_duplicates(sample_df: pd.DataFrame) -> None:
    """Test dropping duplicate rows."""
    df_with_dups = sample_df.copy()
    df_with_dups = pd.concat([df_with_dups, sample_df.iloc[[0]]], ignore_index=True)

    result = transforms.drop_duplicates(df_with_dups)
    assert len(result) == 5


def test_merge_on_column(sample_df: pd.DataFrame) -> None:
    """Test merging dataframes on a common column."""
    left_df = sample_df[["name", "age"]].copy()
    right_df = sample_df[["name", "salary"]].copy()

    result = transforms.merge_dataframes(left_df, right_df, on=["name"])
    assert len(result) == 5
    assert "age" in result.columns
    assert "salary" in result.columns


def test_merge_left_right_on(sample_df: pd.DataFrame) -> None:
    """Test merging dataframes with different column names."""
    left_df = sample_df[["name", "age"]].copy()
    right_df = sample_df[["name", "salary"]].copy()
    right_df = right_df.rename(columns={"name": "person"})

    result = transforms.merge_dataframes(
        left_df, right_df, left_on="name", right_on="person", how="inner"
    )
    assert len(result) == 5
    assert "age" in result.columns
    assert "salary" in result.columns


def test_merge_outer(sample_df: pd.DataFrame) -> None:
    """Test outer merge."""
    left_df = sample_df[["name", "age"]].head(3)
    right_df = sample_df[["name", "salary"]].tail(3)

    result = transforms.merge_dataframes(left_df, right_df, on=["name"], how="outer")
    assert len(result) == 5


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


def test_concat_dataframes(sample_df: pd.DataFrame) -> None:
    """Test concatenating dataframes."""
    df1 = sample_df.head(2)
    df2 = sample_df.tail(2)
    result = transforms.concat_dataframes([df1, df2])
    assert len(result) == 4
    assert list(result.columns) == list(sample_df.columns)
