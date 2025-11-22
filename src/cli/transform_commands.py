"""CLI commands for dataframe transformations."""

from typing import Annotated

import typer

from src.core import io_service, transform_service

app = typer.Typer(add_completion=False)


@app.command()
def select(
    input_file: Annotated[str, typer.Argument(help="Input file path or '-' for stdin")],
    columns: Annotated[list[str], typer.Argument(help="Columns to select")],
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Select specific columns from the dataframe."""
    df = io_service.read_dataframe(input_file)
    result = transform_service.select_columns(df, columns)
    io_service.write_dataframe(result, output)


@app.command()
def drop(
    input_file: Annotated[str, typer.Argument(help="Input file path or '-' for stdin")],
    columns: Annotated[list[str], typer.Argument(help="Columns to drop")],
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Drop specific columns from the dataframe."""
    df = io_service.read_dataframe(input_file)
    result = transform_service.drop_columns(df, columns)
    io_service.write_dataframe(result, output)


@app.command()
def sort(
    input_file: Annotated[str, typer.Argument(help="Input file path or '-' for stdin")],
    columns: Annotated[list[str], typer.Argument(help="Columns to sort by")],
    ascending: Annotated[bool, typer.Option("--ascending/--descending", help="Sort order")] = True,
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Sort dataframe by specified columns."""
    df = io_service.read_dataframe(input_file)
    result = transform_service.sort_by(df, columns, ascending)
    io_service.write_dataframe(result, output)


@app.command()
def dedup(
    input_file: Annotated[str, typer.Argument(help="Input file path or '-' for stdin")],
    subset: Annotated[
        list[str] | None,
        typer.Option("--subset", "-s", help="Columns to consider for duplicates"),
    ] = None,
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Remove duplicate rows from the dataframe."""
    df = io_service.read_dataframe(input_file)
    result = transform_service.drop_duplicates(df, subset)
    io_service.write_dataframe(result, output)


@app.command()
def reset_index(
    input_file: Annotated[str, typer.Argument(help="Input file path or '-' for stdin")],
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Reset the dataframe index."""
    df = io_service.read_dataframe(input_file)
    result = transform_service.reset_index(df)
    io_service.write_dataframe(result, output)
