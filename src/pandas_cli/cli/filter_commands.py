"""CLI commands for dataframe filtering operations."""

from typing import Annotated

import typer

from pandas_cli.cli.options import InputFileArgument, OutputOption, UseJsonOption
from pandas_cli.core import filtering, io_operations

app = typer.Typer(add_completion=False)


@app.command()
def query(
    expression: Annotated[str, typer.Argument(help="Pandas query expression")],
    input_file: InputFileArgument = "-",
    use_json: UseJsonOption = False,
    output: OutputOption = None,
) -> None:
    """Filter dataframe using a pandas query expression."""
    df = io_operations.read_dataframe(input_file)
    result = filtering.filter_by_query(df, expression)
    io_operations.write_dataframe(result, output, use_json)


@app.command()
def head(
    n: Annotated[int, typer.Option("--n", "-n", help="Number of rows")] = 10,
    input_file: InputFileArgument = "-",
    use_json: UseJsonOption = False,
    output: OutputOption = None,
) -> None:
    """Return the first n rows of the dataframe."""
    df = io_operations.read_dataframe(input_file)
    result = filtering.head(df, n)
    io_operations.write_dataframe(result, output, use_json)


@app.command()
def tail(
    n: Annotated[int, typer.Option("--n", "-n", help="Number of rows")] = 10,
    input_file: InputFileArgument = "-",
    use_json: UseJsonOption = False,
    output: OutputOption = None,
) -> None:
    """Return the last n rows of the dataframe."""
    df = io_operations.read_dataframe(input_file)
    result = filtering.tail(df, n)
    io_operations.write_dataframe(result, output, use_json)


@app.command()
def dropna(
    column: Annotated[
        str | None,
        typer.Option(
            "--column", "-c", help="Column to check for null values (default: any column)"
        ),
    ] = None,
    input_file: InputFileArgument = "-",
    use_json: UseJsonOption = False,
    output: OutputOption = None,
) -> None:
    """Remove rows with null values in specified column or any column."""
    df = io_operations.read_dataframe(input_file)
    result = filtering.filter_null(df, column, keep_null=False)
    io_operations.write_dataframe(result, output, use_json)
