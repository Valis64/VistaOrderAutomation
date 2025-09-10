"""Fetch Vista orders and download art files."""
from __future__ import annotations

from pathlib import Path
import re

import typer
from rich.console import Console
from playwright.sync_api import sync_playwright

from services.pom import login, iter_orders, download_art

console = Console()
app = typer.Typer(add_completion=False, help=__doc__)


def sanitize(name: str) -> str:
    """Return filesystem-safe version of *name*."""
    return re.sub(r"[^A-Za-z0-9_-]", "_", name)


@app.command()
def main(
    headless: bool = typer.Option(True, help="Run browser in headless mode."),
    storage: Path = typer.Option(Path("storage_state.json"), help="Storage state path"),
) -> None:
    """Login to POM and download all art files for new orders."""
    orders = 0
    files = 0

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless)
        context = browser.new_context(
            storage_state=str(storage) if storage.exists() else None
        )
        if not storage.exists():
            login(context)
            context.storage_state(path=str(storage))
        page = context.new_page()
        page.goto("https://pom.cimpress.io/items?fulfillerId=n66hf65q8j&status=new")
        for order_id, element in iter_orders(page):
            order_dir = Path("Vista") / sanitize(order_id)
            files += download_art(page, element, order_dir)
            orders += 1
        console.print(f"Processed {orders} orders and {files} files", style="bold")


if __name__ == "__main__":
    app()
