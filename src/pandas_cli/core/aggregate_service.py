"""Service for dataframe aggregation operations."""

import pandas as pd


def value_counts(df: pd.DataFrame, column: str, normalize: bool = False) -> pd.DataFrame:
    """Count unique values in a column."""
    counts = df[column].value_counts(normalize=normalize)
    return counts.reset_index()


def group_by(df: pd.DataFrame, columns: list[str], agg_column: str, agg_func: str) -> pd.DataFrame:
    """Group by columns and apply aggregation function."""
    return df.groupby(columns)[agg_column].agg(agg_func).reset_index()
