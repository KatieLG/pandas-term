"""CLI commands for dataframe transformations."""

from typing import Annotated, Literal

import typer

from pandas_cli.core import io_service, transform_service

app = typer.Typer(add_completion=False)


@app.command()
def select(
    columns: Annotated[str, typer.Argument(help="Comma-separated list of columns to select")],
    input_file: Annotated[str, typer.Argument(help="Input file path (default: stdin)")] = "-",
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Select specific columns from the dataframe."""
    df = io_service.read_dataframe(input_file)
    column_list = [col.strip() for col in columns.split(",")]
    result = transform_service.select_columns(df, column_list)
    io_service.write_dataframe(result, output)


@app.command()
def drop(
    columns: Annotated[str, typer.Argument(help="Comma-separated list of columns to drop")],
    input_file: Annotated[str, typer.Argument(help="Input file path (default: stdin)")] = "-",
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Drop specific columns from the dataframe."""
    df = io_service.read_dataframe(input_file)
    column_list = [col.strip() for col in columns.split(",")]
    result = transform_service.drop_columns(df, column_list)
    io_service.write_dataframe(result, output)


@app.command()
def sort(
    columns: Annotated[str, typer.Argument(help="Comma-separated list of columns to sort by")],
    input_file: Annotated[str, typer.Argument(help="Input file path (default: stdin)")] = "-",
    ascending: Annotated[bool, typer.Option("--ascending/--descending", help="Sort order")] = True,
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Sort dataframe by specified columns."""
    df = io_service.read_dataframe(input_file)
    column_list = [col.strip() for col in columns.split(",")]
    result = transform_service.sort_by(df, column_list, ascending)
    io_service.write_dataframe(result, output)


@app.command()
def dedup(
    input_file: Annotated[str, typer.Argument(help="Input file path (default: stdin)")] = "-",
    subset: Annotated[
        str | None,
        typer.Option(
            "--subset", "-s", help="Comma-separated list of columns to consider for duplicates"
        ),
    ] = None,
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Remove duplicate rows from the dataframe."""
    df = io_service.read_dataframe(input_file)
    subset_list = [col.strip() for col in subset.split(",")] if subset else None
    result = transform_service.drop_duplicates(df, subset_list)
    io_service.write_dataframe(result, output)


@app.command()
def reset_index(
    input_file: Annotated[str, typer.Argument(help="Input file path (default: stdin)")] = "-",
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
        str | None,
        typer.Option("--on", help="Comma-separated list of columns to merge on"),
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
    on_list = [col.strip() for col in on.split(",")] if on else None
    result = transform_service.merge_dataframes(left_df, right_df, on_list, how, left_on, right_on)
    io_service.write_dataframe(result, output)


@app.command()
def batch(
    batch_size: Annotated[int, typer.Argument(help="Number of rows per batch")],
    input_file: Annotated[str, typer.Argument(help="Input file path (default: stdin)")] = "-",
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
