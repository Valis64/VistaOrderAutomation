"""Fetch Vista orders and download art files."""
from __future__ import annotations

import base64
import hashlib
import hmac
import os
import struct
import time
from pathlib import Path
from typing import Optional

import requests
import typer
from rich.console import Console
from tenacity import retry, stop_after_attempt, wait_exponential
from playwright.sync_api import Page, sync_playwright

from automation import selectors

console = Console()
app = typer.Typer(add_completion=False, help=__doc__)


def _totp_code(secret: str) -> str:
    """Generate a TOTP code for the given base32 secret."""
    key = base64.b32decode(secret.upper())
    counter = struct.pack(">Q", int(time.time()) // 30)
    h = hmac.new(key, counter, hashlib.sha1).digest()
    o = h[19] & 0x0F
    token = (struct.unpack(">I", h[o:o + 4])[0] & 0x7FFFFFFF) % 10 ** 6
    return f"{token:06d}"


def choose_nonclobber(path: Path) -> Path:
    """Return a non-clobbering path by adding numeric suffix if needed."""
    base = path
    counter = 1
    while path.exists():
        path = base.with_name(f"{base.stem}-{counter}{base.suffix}")
        counter += 1
    return path


def same_size(path: Path, size: int) -> bool:
    """Check if *path* exists and matches *size*."""
    return path.exists() and path.stat().st_size == size


@retry(wait=wait_exponential(multiplier=1, min=1, max=30), stop=stop_after_attempt(5))
def download_with_retry(url: str, dest: Path, session: requests.Session) -> bool:
    """Download *url* to *dest* if needed; return True if downloaded."""
    resp = session.get(url, stream=True, timeout=60)
    resp.raise_for_status()
    size = int(resp.headers.get("Content-Length", 0))
    etag = resp.headers.get("ETag")
    etag_file = dest.with_suffix(dest.suffix + ".etag")
    if same_size(dest, size) and etag and etag_file.exists() and etag_file.read_text() == etag:
        return False
    tmp = choose_nonclobber(dest)
    with open(tmp, "wb") as fh:
        for chunk in resp.iter_content(chunk_size=8192):
            fh.write(chunk)
    if etag:
        etag_file.write_text(etag)
    return True


def _login(page: Page, username: str, password: str, secret: Optional[str]) -> None:
    page.goto("https://pom.cimpress.io/")
    page.fill(selectors.POM_USERNAME_INPUT, username)
    page.fill(selectors.POM_PASSWORD_INPUT, password)
    page.click(selectors.POM_LOGIN_BUTTON)
    if secret:
        code = _totp_code(secret)
        page.fill(selectors.POM_TOTP_INPUT, code)
        page.click(selectors.POM_TOTP_SUBMIT)
    page.wait_for_load_state("networkidle")


@app.command()
def main(
    headless: bool = typer.Option(True, help="Run browser in headless mode."),
    storage: Path = typer.Option(Path("storage_state.json"), help="Storage state path"),
) -> None:
    """Login to POM and download all art files for new orders."""
    username = os.getenv("POM_USERNAME")
    password = os.getenv("POM_PASSWORD")
    if not username or not password:
        console.print("POM_USERNAME and POM_PASSWORD must be set", style="bold red")
        raise typer.Exit(code=1)
    secret = os.getenv("POM_TOTP_SECRET")

    orders = 0
    files = 0

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless)
        context = browser.new_context(storage_state=str(storage) if storage.exists() else None)
        page = context.new_page()
        if not storage.exists():
            _login(page, username, password, secret)
            context.storage_state(path=str(storage))

        page.goto("https://pom.cimpress.io/items?fulfillerId=n66hf65q8j&status=new")
        session = requests.Session()

        while True:
            page.wait_for_load_state("networkidle")
            rows = page.query_selector_all(selectors.POM_ORDER_ROW)
            if not rows:
                break
            for row in rows:
                oid = row.get_attribute("data-orderid") or row.query_selector(selectors.POM_ORDER_ID).inner_text().strip()
                order_dir = Path("Vista") / oid
                order_dir.mkdir(parents=True, exist_ok=True)
                links = row.query_selector_all(selectors.POM_ART_FILE_LINK)
                for link in links:
                    url = link.get_attribute("href")
                    fname = order_dir / Path(url.split("/")[-1])
                    downloaded = download_with_retry(url, fname, session)
                    action = "downloaded" if downloaded else "skipped"
                    console.log(f"{oid}: {fname.name} {action}")
                    if downloaded:
                        files += 1
                orders += 1
            next_btn = page.query_selector(selectors.POM_NEXT_BUTTON)
            if not next_btn or "disabled" in (next_btn.get_attribute("class") or ""):
                break
            next_btn.click()
        console.print(f"Processed {orders} orders and {files} files", style="bold")


if __name__ == "__main__":
    app()
