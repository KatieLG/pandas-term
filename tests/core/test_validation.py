"""Tests for validation module."""

import pandas as pd
import pytest
import typer

from pandas_term.core.validation import get_columns, validate_columns


def test_validate_columns_valid(sample_df: pd.DataFrame) -> None:
    """Test validating columns that exist."""
    validate_columns(sample_df, ["name", "age"])


def test_validate_columns_missing(sample_df: pd.DataFrame) -> None:
    """Test validating columns that don't exist."""
    with pytest.raises(typer.BadParameter, match="Columns not found"):
        validate_columns(sample_df, ["name", "nonexistent"])


def test_get_columns_parses_and_validates(sample_df: pd.DataFrame) -> None:
    """get_columns parses and validates in one call."""
    result = get_columns(sample_df, "name,age")
    assert result == ["name", "age"]


def test_get_columns_invalid_column(sample_df: pd.DataFrame) -> None:
    """get_columns raises for invalid columns."""
    with pytest.raises(typer.BadParameter, match="Columns not found"):
        get_columns(sample_df, "name,nonexistent")
