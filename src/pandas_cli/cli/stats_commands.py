"""CLI commands for dataframe statistics operations."""

from typing import Annotated

import typer

from pandas_cli.cli.options import InputFileArgument, OutputOption, UseJsonOption
from pandas_cli.core import io_operations, stats

app = typer.Typer(add_completion=False)


@app.command()
def describe(
    input_file: InputFileArgument = "-",
    use_json: UseJsonOption = False,
    output: OutputOption = None,
) -> None:
    """Generate descriptive statistics for the dataframe."""
    df = io_operations.read_dataframe(input_file)
    result = stats.describe(df)
    io_operations.write_dataframe(result, output, use_json)


@app.command()
def unique(
    column: Annotated[str, typer.Argument(help="Column to get unique values from")],
    input_file: InputFileArgument = "-",
) -> None:
    """Display unique values in a column."""
    df = io_operations.read_dataframe(input_file)
    values = stats.unique_values(df, column)
    for value in values:
        typer.echo(value)


@app.command()
def shape(
    input_file: InputFileArgument = "-",
) -> None:
    """Display dimensions (rows, columns) of the dataframe."""
    df = io_operations.read_dataframe(input_file)
    rows, cols = stats.shape(df)
    typer.echo(f"{rows} rows x {cols} columns")


@app.command()
def columns(
    input_file: InputFileArgument = "-",
) -> None:
    """Display column names of the dataframe."""
    df = io_operations.read_dataframe(input_file)
    for col in stats.columns(df):
        typer.echo(col)
