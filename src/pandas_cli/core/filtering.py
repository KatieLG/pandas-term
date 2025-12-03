"""Service for dataframe filtering operations."""

import pandas as pd


def filter_by_query(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Filter dataframe using a pandas query expression."""
    return df.query(query)


def filter_by_value(df: pd.DataFrame, column: str, value: str | int | float) -> pd.DataFrame:
    """Filter rows where column equals a specific value."""
    return df[df[column] == value]


def filter_null(
    df: pd.DataFrame, column: str | None = None, keep_null: bool = False
) -> pd.DataFrame:
    """Filter rows based on null values in specified column or any column."""
    if column:
        if keep_null:
            return df[df[column].isna()]
        return df[df[column].notna()]
    return df.dropna() if not keep_null else df[df.isna().any(axis=1)]


def head(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the first n rows."""
    return df.head(n)


def tail(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the last n rows."""
    return df.tail(n)


def sample(
    df: pd.DataFrame,
    n: int | None = None,
    frac: float | None = None,
    seed: int | None = None,
) -> pd.DataFrame:
    """Return a random sample of rows."""
    return df.sample(n=n, frac=frac, random_state=seed)
