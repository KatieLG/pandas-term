"""Service for dataframe transformation operations."""

from typing import Literal

import pandas as pd


def select_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Select specific columns from the dataframe."""
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Columns not found: {', '.join(missing)}")
    return df[columns]


def drop_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Drop specific columns from the dataframe."""
    existing = [col for col in columns if col in df.columns]
    return df.drop(columns=existing)


def rename_columns(df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    """Rename columns using a mapping dictionary."""
    return df.rename(columns=mapping)


def sort_by(df: pd.DataFrame, columns: list[str], ascending: bool = True) -> pd.DataFrame:
    """Sort dataframe by specified columns."""
    return df.sort_values(by=columns, ascending=ascending)


def drop_duplicates(df: pd.DataFrame, subset: list[str] | None = None) -> pd.DataFrame:
    """Remove duplicate rows."""
    return df.drop_duplicates(subset=subset)


def merge_dataframes(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    on: list[str] | None = None,
    how: Literal["inner", "left", "right", "outer", "cross"] = "inner",
    left_on: str | None = None,
    right_on: str | None = None,
) -> pd.DataFrame:
    """Merge two dataframes."""
    if left_on and right_on:
        return left_df.merge(right_df, left_on=left_on, right_on=right_on, how=how)
    return left_df.merge(right_df, on=on, how=how)


def batch_dataframe(df: pd.DataFrame, batch_size: int) -> list[pd.DataFrame]:
    """Split dataframe into batches of specified size."""
    num_batches = len(df) // batch_size + (1 if len(df) % batch_size != 0 else 0)
    return [df.iloc[i * batch_size : (i + 1) * batch_size] for i in range(num_batches)]


def concat_dataframes(dfs: list[pd.DataFrame], ignore_index: bool = True) -> pd.DataFrame:
    """Concatenate multiple dataframes vertically."""
    return pd.concat(dfs, ignore_index=ignore_index)
