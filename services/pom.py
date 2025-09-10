"""Helpers for interacting with POM (Cimpress) portal."""
from __future__ import annotations

import base64
import hashlib
import hmac
import os
import re
import struct
import time
from pathlib import Path
from typing import Iterator, Tuple

import requests
from playwright.sync_api import BrowserContext, ElementHandle, Page
from rich.console import Console
from tenacity import retry, stop_after_attempt, wait_exponential

from automation import selectors

console = Console()


def _totp_code(secret: str) -> str:
    """Generate a TOTP code for the given base32 secret."""
    key = base64.b32decode(secret.upper())
    counter = struct.pack(">Q", int(time.time()) // 30)
    h = hmac.new(key, counter, hashlib.sha1).digest()
    o = h[19] & 0x0F
    token = (struct.unpack(">I", h[o:o + 4])[0] & 0x7FFFFFFF) % 10 ** 6
    return f"{token:06d}"


def _choose_nonclobber(path: Path) -> Path:
    """Return a non-clobbering path by adding numeric suffix if needed."""
    base = path
    counter = 1
    while path.exists():
        path = base.with_name(f"{base.stem}-{counter}{base.suffix}")
        counter += 1
    return path


def _same_size(path: Path, size: int) -> bool:
    """Check if *path* exists and matches *size*."""
    return path.exists() and path.stat().st_size == size


@retry(wait=wait_exponential(multiplier=1, min=1, max=30), stop=stop_after_attempt(5))
def _download_with_retry(url: str, dest: Path, session: requests.Session) -> bool:
    """Download *url* to *dest* if needed; return True if downloaded."""
    resp = session.get(url, stream=True, timeout=60)
    resp.raise_for_status()
    size = int(resp.headers.get("Content-Length", 0))
    etag = resp.headers.get("ETag")
    etag_file = dest.with_suffix(dest.suffix + ".etag")
    if _same_size(dest, size) and etag and etag_file.exists() and etag_file.read_text() == etag:
        return False
    tmp = _choose_nonclobber(dest)
    with open(tmp, "wb") as fh:
        for chunk in resp.iter_content(chunk_size=8192):
            fh.write(chunk)
    if etag:
        etag_file.write_text(etag)
    return True


def login(context: BrowserContext) -> None:
    """Ensure we are authenticated to POM using environment credentials."""
    username = os.getenv("POM_USERNAME")
    password = os.getenv("POM_PASSWORD")
    if not username or not password:
        raise ValueError("POM_USERNAME and POM_PASSWORD must be set")
    secret = os.getenv("POM_TOTP_SECRET")

    page = context.new_page()
    # Navigate to the POM portal which will redirect to the Auth0 login page.
    page.goto("https://pom.cimpress.io/")
    # Wait for the redirect to the actual login URL before interacting.
    page.wait_for_url(re.compile(r"https://cimpress\.auth0\.com/.*"))
    page.fill(selectors.POM_USERNAME_INPUT, username)
    page.fill(selectors.POM_PASSWORD_INPUT, password)
    page.click(selectors.POM_SUBMIT_BUTTON)
    if secret:
        page.fill(selectors.POM_TOTP_INPUT, _totp_code(secret))
        page.click(selectors.POM_TOTP_SUBMIT)
    page.wait_for_load_state("networkidle")
    page.close()


def iter_orders(page: Page) -> Iterator[Tuple[str, ElementHandle]]:
    """Yield ``(order_id, element)`` pairs for all orders across pages."""
    while True:
        page.wait_for_load_state("networkidle")
        rows = page.query_selector_all(selectors.POM_ORDER_ROW)
        for row in rows:
            oid = row.get_attribute("data-orderid") or row.query_selector(
                selectors.POM_ORDER_ROW_ID_LABEL
            ).inner_text().strip()
            yield oid, row
        next_btn = page.query_selector(selectors.POM_NEXT_PAGE_BUTTON)
        if not next_btn or "disabled" in (next_btn.get_attribute("class") or ""):
            break
        next_btn.click()


def download_art(page: Page, order: ElementHandle, dest_dir: Path) -> int:
    """Download all art assets for *order* into *dest_dir*.

    Returns the number of files downloaded.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    links = order.query_selector_all(selectors.POM_ART_DOWNLOAD_LINK)
    session = requests.Session()
    count = 0
    for link in links:
        url = link.get_attribute("href")
        if not url:
            continue
        fname = dest_dir / Path(url.split("/")[-1])
        downloaded = _download_with_retry(url, fname, session)
        action = "downloaded" if downloaded else "skipped"
        console.log(f"{dest_dir.name}: {fname.name} {action}")
        if downloaded:
            count += 1
    return count
