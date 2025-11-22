"""Service for dataframe transformation operations."""

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


def add_column(df: pd.DataFrame, name: str, expression: str) -> pd.DataFrame:
    """Add a new column based on an expression."""
    df = df.copy()
    df[name] = df.eval(expression)
    return df


def drop_duplicates(df: pd.DataFrame, subset: list[str] | None = None) -> pd.DataFrame:
    """Remove duplicate rows."""
    return df.drop_duplicates(subset=subset)


def reset_index(df: pd.DataFrame) -> pd.DataFrame:
    """Reset the dataframe index."""
    return df.reset_index(drop=True)
