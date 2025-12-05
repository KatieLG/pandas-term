"""Tests for parsing utilities."""

from pandas_term.core import parsing


def test_parse_columns_single() -> None:
    """Parse a single column name."""
    assert parsing.parse_columns("name") == ["name"]


def test_parse_columns_multiple() -> None:
    """Parse multiple comma-separated column names."""
    assert parsing.parse_columns("name,age,city") == ["name", "age", "city"]


def test_parse_columns_with_whitespace() -> None:
    """Parse columns with surrounding whitespace."""
    assert parsing.parse_columns("name , age , city") == ["name", "age", "city"]


def test_parse_columns_none() -> None:
    """Return None when input is None."""
    assert parsing.parse_columns(None) is None
