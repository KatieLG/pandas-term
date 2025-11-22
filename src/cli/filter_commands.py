"""CLI commands for dataframe filtering operations."""

from typing import Annotated

import typer

from src.core import filter_service, io_service

app = typer.Typer(add_completion=False)


@app.command()
def query(
    input_file: Annotated[str, typer.Argument(help="Input file path or '-' for stdin")],
    expression: Annotated[str, typer.Argument(help="Pandas query expression")],
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Filter dataframe using a pandas query expression."""
    df = io_service.read_dataframe(input_file)
    result = filter_service.filter_by_query(df, expression)
    io_service.write_dataframe(result, output)


@app.command()
def head(
    input_file: Annotated[str, typer.Argument(help="Input file path or '-' for stdin")],
    n: Annotated[int, typer.Option("--n", "-n", help="Number of rows")] = 10,
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Return the first n rows of the dataframe."""
    df = io_service.read_dataframe(input_file)
    result = filter_service.head(df, n)
    io_service.write_dataframe(result, output)


@app.command()
def tail(
    input_file: Annotated[str, typer.Argument(help="Input file path or '-' for stdin")],
    n: Annotated[int, typer.Option("--n", "-n", help="Number of rows")] = 10,
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Return the last n rows of the dataframe."""
    df = io_service.read_dataframe(input_file)
    result = filter_service.tail(df, n)
    io_service.write_dataframe(result, output)


@app.command()
def sample(
    input_file: Annotated[str, typer.Argument(help="Input file path or '-' for stdin")],
    n: Annotated[int | None, typer.Option("--n", "-n", help="Number of rows to sample")] = None,
    frac: Annotated[
        float | None, typer.Option("--frac", "-f", help="Fraction of rows to sample")
    ] = None,
    seed: Annotated[int | None, typer.Option("--seed", "-s", help="Random seed")] = None,
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Return a random sample of rows from the dataframe."""
    df = io_service.read_dataframe(input_file)
    result = filter_service.sample(df, n, frac, seed)
    io_service.write_dataframe(result, output)


@app.command()
def dropna(
    input_file: Annotated[str, typer.Argument(help="Input file path or '-' for stdin")],
    column: Annotated[str, typer.Argument(help="Column to check for null values")],
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Remove rows with null values in the specified column."""
    df = io_service.read_dataframe(input_file)
    result = filter_service.filter_null(df, column, keep_null=False)
    io_service.write_dataframe(result, output)
