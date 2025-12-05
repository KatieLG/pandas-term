import sys

import typer

from pandas_term.cli import aggregate_commands, filter_commands, stats_commands, transform_commands
from pandas_term.cli.options import (
    AppContext,
    FormatOption,
    OutputOption,
    OutputOptions,
    UseJsonOption,
)

app = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]})


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    use_json: UseJsonOption = False,
    output: OutputOption = None,
    fmt: FormatOption = None,
) -> None:
    if use_json and fmt is not None:
        raise typer.BadParameter("Cannot specify both --json and --format")
    output_format = fmt or ("json" if use_json else "csv")
    ctx.obj = AppContext(output=OutputOptions(file=output, format=output_format))
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())


app.add_typer(transform_commands.app)
app.add_typer(filter_commands.app)
app.add_typer(stats_commands.app)
app.add_typer(aggregate_commands.app)


def cli() -> None:
    """Run cli with a catch all error display"""
    try:
        app()
    except Exception as e:
        typer.echo(typer.style(f"Error: {e}", fg=typer.colors.RED), err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
