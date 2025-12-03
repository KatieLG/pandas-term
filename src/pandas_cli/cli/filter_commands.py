"""CLI commands for dataframe filtering operations."""

from typing import Annotated

import typer

from pandas_cli.cli.options import FormatOption, InputFileArgument, OutputOption
from pandas_cli.core import filter_service, io_service

app = typer.Typer(add_completion=False)


@app.command()
def query(
    expression: Annotated[str, typer.Argument(help="Pandas query expression")],
    input_file: InputFileArgument = "-",
    fmt: FormatOption = "csv",
    output: OutputOption = None,
) -> None:
    """Filter dataframe using a pandas query expression."""
    df = io_service.read_dataframe(input_file)
    result = filter_service.filter_by_query(df, expression)
    io_service.write_dataframe(result, output, fmt)


@app.command()
def head(
    n: Annotated[int, typer.Option("--n", "-n", help="Number of rows")] = 10,
    input_file: InputFileArgument = "-",
    fmt: FormatOption = "csv",
    output: OutputOption = None,
) -> None:
    """Return the first n rows of the dataframe."""
    df = io_service.read_dataframe(input_file)
    result = filter_service.head(df, n)
    io_service.write_dataframe(result, output, fmt)


@app.command()
def tail(
    n: Annotated[int, typer.Option("--n", "-n", help="Number of rows")] = 10,
    input_file: InputFileArgument = "-",
    fmt: FormatOption = "csv",
    output: OutputOption = None,
) -> None:
    """Return the last n rows of the dataframe."""
    df = io_service.read_dataframe(input_file)
    result = filter_service.tail(df, n)
    io_service.write_dataframe(result, output, fmt)


@app.command()
def sample(
    n: Annotated[int | None, typer.Option("--n", "-n", help="Number of rows to sample")] = None,
    frac: Annotated[float | None, typer.Option("--frac", help="Fraction of rows to sample")] = None,
    seed: Annotated[int | None, typer.Option("--seed", "-s", help="Random seed")] = None,
    input_file: InputFileArgument = "-",
    fmt: FormatOption = "csv",
    output: OutputOption = None,
) -> None:
    """Return a random sample of rows from the dataframe."""
    df = io_service.read_dataframe(input_file)
    result = filter_service.sample(df, n, frac, seed)
    io_service.write_dataframe(result, output, fmt)


@app.command()
def dropna(
    column: Annotated[
        str | None,
        typer.Option(
            "--column", "-c", help="Column to check for null values (default: any column)"
        ),
    ] = None,
    input_file: InputFileArgument = "-",
    fmt: FormatOption = "csv",
    output: OutputOption = None,
) -> None:
    """Remove rows with null values in specified column or any column."""
    df = io_service.read_dataframe(input_file)
    result = filter_service.filter_null(df, column, keep_null=False)
    io_service.write_dataframe(result, output, fmt)
