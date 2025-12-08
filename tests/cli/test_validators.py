import pandas as pd
import pytest
import typer

from pandas_term.cli.validators import (
    get_columns,
    positive_int_list,
    valid_batch_pattern,
    validate_columns,
)


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


@pytest.mark.parametrize("value", ["1", "1393", "88819379172"])
def test_positive_int_valid(value: str) -> None:
    positive_int_list(value)


@pytest.mark.parametrize("value", ["-1", "-9", "0"])
def test_positive_int_invalid(value: str) -> None:
    with pytest.raises(typer.BadParameter, match="not a valid list"):
        positive_int_list(value)


@pytest.mark.parametrize("sizes", ["1", "1,2", "1,2,3", "9,123", "21938"])
def test_positive_int_list_valid(sizes: str) -> None:
    positive_int_list(sizes)


@pytest.mark.parametrize("sizes", ["", "0", "-1", "1,2,3,-4", "-1,2,3,4", "-1 9", "1 9"])
def test_positive_int_list_invalid(sizes: str) -> None:
    with pytest.raises(typer.BadParameter, match="not a valid list"):
        positive_int_list(sizes)


@pytest.mark.parametrize(
    "format,expected_error",
    [
        ("batch_{}_{}.csv", "Invalid output pattern"),
        ("batch_{}", "Output file must have an extension"),
        ("batch{s}", "Invalid output pattern"),
        ("batch_{}.invalid_extension", "Unsupported extension"),
    ],
)
def test_invalid_batch_output(format: str, expected_error: str) -> None:
    with pytest.raises(typer.BadParameter, match=expected_error):
        valid_batch_pattern(format)
