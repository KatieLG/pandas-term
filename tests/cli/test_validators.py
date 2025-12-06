import pandas as pd
import pytest
import typer

from pandas_term.cli.validators import get_columns, validate_columns


def test_validate_columns_valid(sample_df: pd.DataFrame) -> None:
    validate_columns(sample_df, ["name", "age"])


def test_validate_columns_missing(sample_df: pd.DataFrame) -> None:
    with pytest.raises(typer.BadParameter, match="Columns not found"):
        validate_columns(sample_df, ["name", "nonexistent"])


def test_get_columns_valid(sample_df: pd.DataFrame) -> None:
    result = get_columns(sample_df, "name,age")
    assert result == ["name", "age"]


def test_get_columns_invalid_column(sample_df: pd.DataFrame) -> None:
    with pytest.raises(typer.BadParameter, match="Columns not found"):
        get_columns(sample_df, "name,nonexistent")
