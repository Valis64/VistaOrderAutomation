"""Command-line interface for Vista Order Automation."""
from __future__ import annotations

from datetime import date
from typing import Optional

import typer
from rich.console import Console

from config.credentials import load_credentials
from gui.main import main as gui_main
from services.crimpress import login as crimpress_login

app = typer.Typer(help="Vista Order Automation CLI")
console = Console()


@app.command()
def gui() -> None:
    """Launch the graphical user interface."""
    gui_main()


@app.command()
def login() -> None:
    """Attempt Crimpress login with stored credentials."""
    email, password = load_credentials()
    if not email or not password:
        console.print("Credentials not found", style="red")
        raise typer.Exit(code=1)
    try:
        success = crimpress_login(email, password)
    except Exception as exc:  # pragma: no cover - network errors
        console.print(f"Login failed: {exc}", style="red")
        raise typer.Exit(code=1)
    if success:
        console.print("Login successful", style="green")
    else:
        console.print("Login failed", style="red")
        raise typer.Exit(code=1)


@app.command()
def fetch(
    headful: bool = typer.Option(False, help="Run browser with a visible UI."),
    only: Optional[str] = typer.Option(None, "--only", metavar="ORDER_ID", help="Fetch a single order by ID."),
    since: Optional[date] = typer.Option(
        None,
        "--since",
        metavar="YYYY-MM-DD",
        formats=["%Y-%m-%d"],
        help="Fetch orders since this date.",
    ),
) -> None:
    """Fetch Vista orders and download art files."""
    import vista_fetch

    # Mirror progress logs in this console
    vista_fetch.console = console
    vista_fetch.main(headless=not headful, only=only, since=since)


if __name__ == "__main__":
    app()
