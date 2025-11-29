"""CLI commands for dataframe transformations."""

from typing import Annotated, Literal

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


@app.command()
def merge(
    left_file: Annotated[str, typer.Argument(help="Left dataframe file path")],
    right_file: Annotated[str, typer.Argument(help="Right dataframe file path")],
    on: Annotated[
        list[str] | None,
        typer.Option("--on", help="Columns to merge on"),
    ] = None,
    how: Annotated[
        Literal["inner", "left", "right", "outer", "cross"],
        typer.Option("--how", help="Type of merge: inner, left, right, outer, cross"),
    ] = "inner",
    left_on: Annotated[
        str | None,
        typer.Option("--left-on", help="Left dataframe column to merge on"),
    ] = None,
    right_on: Annotated[
        str | None,
        typer.Option("--right-on", help="Right dataframe column to merge on"),
    ] = None,
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Merge two dataframes."""
    left_df = io_service.read_dataframe(left_file)
    right_df = io_service.read_dataframe(right_file)
    result = transform_service.merge_dataframes(left_df, right_df, on, how, left_on, right_on)
    io_service.write_dataframe(result, output)


@app.command()
def batch(
    input_file: Annotated[str, typer.Argument(help="Input file path or '-' for stdin")],
    batch_size: Annotated[int, typer.Argument(help="Number of rows per batch")],
    output_pattern: Annotated[
        str,
        typer.Option("--output", "-o", help="Output file pattern (e.g., 'batch_{}.csv')"),
    ] = "batch_{}.csv",
) -> None:
    """Split dataframe into batches and write to separate files."""
    df = io_service.read_dataframe(input_file)
    batches = transform_service.batch_dataframe(df, batch_size)

    for i, batch_df in enumerate(batches):
        output_file = output_pattern.format(i)
        io_service.write_dataframe(batch_df, output_file)
        typer.echo(f"Written batch {i} to {output_file} ({len(batch_df)} rows)")
