"""Command-line interface for Vista Order Automation."""
from __future__ import annotations

import typer
from rich.console import Console

from config.credentials import load_credentials
from config.settings import load_settings
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
    settings = load_settings()
    login_url = settings.get("login_url", "")
    try:
        success = crimpress_login(email, password, login_url)
    except Exception as exc:  # pragma: no cover - network errors
        console.print(f"Login failed: {exc}", style="red")
        raise typer.Exit(code=1)
    if success:
        console.print("Login successful", style="green")
    else:
        console.print("Login failed", style="red")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
