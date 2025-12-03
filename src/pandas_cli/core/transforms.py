"""Service for dataframe transformation operations."""

import pandas as pd


def validate_columns(df: pd.DataFrame, columns: list[str]) -> None:
    """Validate that all columns exist in the dataframe."""
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Columns not found: {', '.join(missing)}")


def batch_dataframe(df: pd.DataFrame, batch_size: int) -> list[pd.DataFrame]:
    """Split dataframe into batches of specified size."""
    num_batches = len(df) // batch_size + (1 if len(df) % batch_size != 0 else 0)
    return [df.iloc[i * batch_size : (i + 1) * batch_size] for i in range(num_batches)]
