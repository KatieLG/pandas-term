"""Shared CLI options for all commands."""

from dataclasses import dataclass
from typing import Annotated, Literal

import typer

OutputFormat = Literal["csv", "json", "tsv", "md"]


@dataclass
class OutputOptions:
    """Options for outputting dataframes."""

    file: str | None = None
    format: OutputFormat = "csv"


@dataclass
class AppContext:
    """App context passed to all subcommands via ctx.obj."""

    output: OutputOptions


InputFileArgument = Annotated[
    str,
    typer.Argument(help="Input file path (default: stdin)"),
]

UseJsonOption = Annotated[
    bool,
    typer.Option("--json", "-j", help="Output as JSON (shorthand for --format json)"),
]

FormatOption = Annotated[
    OutputFormat | None,
    typer.Option("--format", "-f", help="Output format: csv, json, tsv, md"),
]

OutputOption = Annotated[
    str | None,
    typer.Option("--output", "-o", help="Output file path (default: stdout)"),
]
