"""Shared CLI options for all commands."""

from typing import Annotated, Literal

import typer

InputFileArgument = Annotated[
    str,
    typer.Argument(help="Input file path (default: stdin)"),
]

FormatOption = Annotated[
    Literal["csv", "json"],
    typer.Option("--format", "-f", help="Output format for stdout (default: csv)"),
]

OutputOption = Annotated[
    str | None,
    typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
]
