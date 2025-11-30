"""CLI commands for dataframe statistics operations."""

from typing import Annotated

import typer

from pandas_cli.core import io_service, stats_service

app = typer.Typer(add_completion=False)


@app.command()
def describe(
    input_file: Annotated[str, typer.Argument(help="Input file path or '-' for stdin")],
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Generate descriptive statistics for the dataframe."""
    df = io_service.read_dataframe(input_file)
    result = stats_service.describe(df)
    io_service.write_dataframe(result, output)


@app.command()
def info(
    input_file: Annotated[str, typer.Argument(help="Input file path or '-' for stdin")],
) -> None:
    """Display a concise summary of the dataframe."""
    df = io_service.read_dataframe(input_file)
    info_text = stats_service.info(df)
    typer.echo(info_text)


@app.command()
def value_counts(
    input_file: Annotated[str, typer.Argument(help="Input file path or '-' for stdin")],
    column: Annotated[str, typer.Argument(help="Column to count values in")],
    normalize: Annotated[
        bool,
        typer.Option("--normalize", "-n", help="Return proportions instead of counts"),
    ] = False,
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Count unique values in a column."""
    df = io_service.read_dataframe(input_file)
    result = stats_service.value_counts(df, column, normalize)
    io_service.write_dataframe(result, output)


@app.command()
def groupby(
    input_file: Annotated[str, typer.Argument(help="Input file path or '-' for stdin")],
    group_cols: Annotated[list[str], typer.Argument(help="Columns to group by")],
    col: Annotated[str, typer.Option("--col", "-c", help="Column to aggregate")],
    agg: Annotated[
        str,
        typer.Option("--agg", "-a", help="Aggregation function (sum, mean, count, etc.)"),
    ] = "sum",
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path or '-' for stdout"),
    ] = None,
) -> None:
    """Group by columns and apply aggregation function."""
    df = io_service.read_dataframe(input_file)
    result = stats_service.group_by(df, group_cols, col, agg)
    io_service.write_dataframe(result, output)


@app.command()
def unique(
    input_file: Annotated[str, typer.Argument(help="Input file path or '-' for stdin")],
    column: Annotated[str, typer.Argument(help="Column to get unique values from")],
) -> None:
    """Display unique values in a column."""
    df = io_service.read_dataframe(input_file)
    values = stats_service.unique_values(df, column)
    for value in values:
        typer.echo(value)
