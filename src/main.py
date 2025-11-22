"""Main entry point for pandas-cli."""

import typer

from src.cli import filter_commands, stats_commands, transform_commands

app = typer.Typer(add_completion=False)

app.add_typer(transform_commands.app)
app.add_typer(filter_commands.app)
app.add_typer(stats_commands.app)


if __name__ == "__main__":
    app()
