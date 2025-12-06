"""CLI argument and option validators."""

from pathlib import Path
from typing import Literal, get_args, overload

import pandas as pd
import typer

OutputFormat = Literal["csv", "json", "tsv", "md", "markdown", "xlsx", "xls"]
VALID_EXTENSIONS = {f".{fmt}" for fmt in get_args(OutputFormat)}
VALID_MSG = f"Valid: {', '.join(VALID_EXTENSIONS)}"


def positive_int(value: int) -> int:
    """Validate the input value is positive."""
    if value <= 0:
        raise typer.BadParameter("Must be a positive integer")
    return value


def positive_int_list(value: str) -> str:
    """Validate the comma-separated string contains only positive integers."""
    if all(num.isdigit() and int(num) > 0 for num in value.split(",")):
        return value
    raise typer.BadParameter(f"{value} is not a valid list of positive integers")


def valid_input_file(value: str) -> str:
    """Validate input file exists and has supported extension."""
    if value == "-":
        return value
    path = Path(value)
    if not path.exists():
        raise typer.BadParameter(f"File not found: {value}")
    ext = path.suffix.lower()
    if ext not in VALID_EXTENSIONS:
        raise typer.BadParameter(f"Unsupported extension '{ext}'. {VALID_MSG}")
    return value


def valid_output_file(value: str | None) -> str | None:
    """Validate output file has supported extension."""
    if value is None:
        return None
    parts = value.split(".")
    ext = f".{parts[-1].lower()}"
    if len(parts) < 2:
        raise typer.BadParameter(f"Output file must have an extension. {VALID_MSG}")
    if ext not in VALID_EXTENSIONS:
        raise typer.BadParameter(f"Unsupported extension '{ext}'. {VALID_MSG}")
    return value


def _parse_columns(columns: str) -> list[str]:
    """Parse a comma-separated string of column names into a list."""
    return [col.strip() for col in columns.split(",")]


def validate_columns(df: pd.DataFrame, columns: list[str]) -> None:
    """Validate that all columns exist in the dataframe."""
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise typer.BadParameter(f"Columns not found: {', '.join(missing)}")


@overload
def get_columns(df: pd.DataFrame, columns: str) -> list[str]: ...
@overload
def get_columns(df: pd.DataFrame, columns: None) -> None: ...
def get_columns(df: pd.DataFrame, columns: str | None) -> list[str] | None:
    """Parse comma-separated columns and validate they exist in the dataframe."""
    if columns is None:
        return None
    cols = _parse_columns(columns)
    validate_columns(df, cols)
    return cols
