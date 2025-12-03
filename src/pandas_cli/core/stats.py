"""Service for dataframe statistics operations."""

import pandas as pd


def describe(df: pd.DataFrame) -> pd.DataFrame:
    """Generate descriptive statistics."""
    return df.describe()


def unique_values(df: pd.DataFrame, column: str) -> list:
    """Get unique values in a column."""
    return df[column].unique().tolist()


def shape(df: pd.DataFrame) -> tuple[int, int]:
    """Get dimensions (rows, columns)."""
    return df.shape


def columns(df: pd.DataFrame) -> list[str]:
    """Get column names."""
    return df.columns.tolist()
