"""Shared CLI options for all commands."""

from dataclasses import dataclass
from typing import Annotated

import typer


@dataclass
class OutputOptions:
    """Options for outputting dataframes."""

    file: str | None = None
    use_json: bool = False


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
    typer.Option("--json", "-j", help="Output as JSON instead of CSV"),
]

OutputOption = Annotated[
    str | None,
    typer.Option("--output", "-o", help="Output file path (default: stdout)"),
]
