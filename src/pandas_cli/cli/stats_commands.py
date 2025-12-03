"""CLI commands for dataframe statistics operations."""

from typing import Annotated

import typer

from pandas_cli.cli.options import FormatOption, InputFileArgument, OutputOption
from pandas_cli.core import io_service, stats_service

app = typer.Typer(add_completion=False)


@app.command()
def describe(
    input_file: InputFileArgument = "-",
    fmt: FormatOption = "csv",
    output: OutputOption = None,
) -> None:
    """Generate descriptive statistics for the dataframe."""
    df = io_service.read_dataframe(input_file)
    result = stats_service.describe(df)
    io_service.write_dataframe(result, output, fmt)


@app.command()
def info(
    input_file: InputFileArgument = "-",
) -> None:
    """Display a concise summary of the dataframe."""
    df = io_service.read_dataframe(input_file)
    info_text = stats_service.info(df)
    typer.echo(info_text)


@app.command()
def value_counts(
    column: Annotated[str, typer.Argument(help="Column to count values in")],
    input_file: InputFileArgument = "-",
    normalize: Annotated[
        bool,
        typer.Option("--normalize", "-n", help="Return proportions instead of counts"),
    ] = False,
    fmt: FormatOption = "csv",
    output: OutputOption = None,
) -> None:
    """Count unique values in a column."""
    df = io_service.read_dataframe(input_file)
    result = stats_service.value_counts(df, column, normalize)
    io_service.write_dataframe(result, output, fmt)


@app.command()
def groupby(
    group_cols: Annotated[str, typer.Argument(help="Comma-separated list of columns to group by")],
    input_file: InputFileArgument = "-",
    col: Annotated[str | None, typer.Option("--col", "-c", help="Column to aggregate")] = None,
    agg: Annotated[
        str,
        typer.Option("--agg", "-a", help="Aggregation function (sum, mean, count, etc.)"),
    ] = "sum",
    fmt: FormatOption = "csv",
    output: OutputOption = None,
) -> None:
    """Group by columns and apply aggregation function."""
    if col is None:
        raise typer.BadParameter("--col is required")
    df = io_service.read_dataframe(input_file)
    group_col_list = [col.strip() for col in group_cols.split(",")]
    result = stats_service.group_by(df, group_col_list, col, agg)
    io_service.write_dataframe(result, output, fmt)


@app.command()
def unique(
    column: Annotated[str, typer.Argument(help="Column to get unique values from")],
    input_file: InputFileArgument = "-",
) -> None:
    """Display unique values in a column."""
    df = io_service.read_dataframe(input_file)
    values = stats_service.unique_values(df, column)
    for value in values:
        typer.echo(value)
