"""Service for dataframe statistics operations."""

import io

import pandas as pd


def describe(df: pd.DataFrame) -> pd.DataFrame:
    """Generate descriptive statistics."""
    return df.describe()


def info(df: pd.DataFrame) -> str:
    """Generate a concise summary of the dataframe."""
    buffer = io.StringIO()
    df.info(buf=buffer)
    return buffer.getvalue()


def unique_values(df: pd.DataFrame, column: str) -> list:
    """Get unique values in a column."""
    return df[column].unique().tolist()


def size(df: pd.DataFrame) -> int:
    """Get total number of elements."""
    return df.size


def shape(df: pd.DataFrame) -> tuple[int, int]:
    """Get dimensions (rows, columns)."""
    return df.shape


def columns(df: pd.DataFrame) -> list[str]:
    """Get column names."""
    return df.columns.tolist()


def memory_usage(df: pd.DataFrame, deep: bool = False) -> pd.Series:
    """Get memory usage of each column."""
    return df.memory_usage(deep=deep)
