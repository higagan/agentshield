"""Command-line interface for ModelFuzz."""

import typer

from modelfuzz import __version__

app = typer.Typer(help="Runtime guardrails for AI agents.")


@app.callback()
def cli() -> None:
    """Runtime guardrails for AI agents."""


@app.command()
def version() -> None:
    """Print the installed ModelFuzz version."""
    typer.echo(__version__)


def main() -> None:
    """Entry point for the ``modelfuzz`` console script."""
    app()


if __name__ == "__main__":
    main()
