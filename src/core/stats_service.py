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


def value_counts(df: pd.DataFrame, column: str, normalize: bool = False) -> pd.DataFrame:
    """Count unique values in a column."""
    counts = df[column].value_counts(normalize=normalize)
    return counts.reset_index()


def group_by(df: pd.DataFrame, columns: list[str], agg_column: str, agg_func: str) -> pd.DataFrame:
    """Group by columns and apply aggregation function."""
    return df.groupby(columns)[agg_column].agg(agg_func).reset_index()


def correlation(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Calculate correlation matrix."""
    if columns:
        return df[columns].corr()
    return df.select_dtypes(include=["number"]).corr()


def unique_values(df: pd.DataFrame, column: str) -> list:
    """Get unique values in a column."""
    return df[column].unique().tolist()


def missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Show missing values count and percentage for each column."""
    total = len(df)
    missing = df.isna().sum()
    percent = (missing / total * 100).round(2)

    result = pd.DataFrame(
        {
            "column": missing.index,
            "missing_count": missing.to_numpy(),
            "missing_percent": percent.to_numpy(),
        }
    )

    return result[result["missing_count"] > 0]
