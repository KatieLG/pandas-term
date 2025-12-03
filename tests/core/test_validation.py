"""Tests for validation module."""

import pandas as pd
import pytest

from pandas_term.core import validation


def test_validate_columns_valid(sample_df: pd.DataFrame) -> None:
    """Test validating columns that exist."""
    validation.validate_columns(sample_df, ["name", "age"])


def test_validate_columns_missing(sample_df: pd.DataFrame) -> None:
    """Test validating columns that don't exist."""
    with pytest.raises(ValueError, match="Columns not found"):
        validation.validate_columns(sample_df, ["name", "nonexistent"])
