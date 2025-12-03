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
def info(
    input_file: InputFileArgument = "-",
) -> None:
    """Display a concise summary of the dataframe."""
    df = io_operations.read_dataframe(input_file)
    info_text = stats.info(df)
    typer.echo(info_text)


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
def size(
    input_file: InputFileArgument = "-",
) -> None:
    """Display total number of elements in the dataframe."""
    df = io_operations.read_dataframe(input_file)
    typer.echo(stats.size(df))


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


@app.command()
def memory(
    input_file: InputFileArgument = "-",
    deep: Annotated[
        bool, typer.Option("--deep", "-d", help="Introspect data deeply for accurate memory usage")
    ] = False,
) -> None:
    """Display memory usage of each column."""
    df = io_operations.read_dataframe(input_file)
    usage = stats.memory_usage(df, deep=deep)
    typer.echo(usage.to_string())
