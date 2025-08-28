"""Automation helpers for Crimpress login."""
from __future__ import annotations

import os
from tenacity import retry, stop_after_attempt, wait_fixed
from playwright.sync_api import Error, sync_playwright
from rich.console import Console

from automation.selectors import (
    CRIMPRESS_EMAIL_INPUT,
    CRIMPRESS_PASSWORD_INPUT,
    CRIMPRESS_SUBMIT_BUTTON,
)

console = Console()
LOGIN_URL = os.environ.get("CRIMPRESS_LOGIN_URL", "")


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def login(email: str, password: str) -> bool:
    """Attempt to authenticate to Crimpress."""
    if not LOGIN_URL:
        raise ValueError("CRIMPRESS_LOGIN_URL not set")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        console.log("Navigating to Crimpress login")
        page.goto(LOGIN_URL)
        page.fill(CRIMPRESS_EMAIL_INPUT, email)
        page.fill(CRIMPRESS_PASSWORD_INPUT, password)
        page.click(CRIMPRESS_SUBMIT_BUTTON)
        try:
            page.wait_for_load_state("networkidle")
        except Error:
            console.log("Network idle wait timed out", style="red")
            browser.close()
            return False
        success = not page.locator(CRIMPRESS_EMAIL_INPUT).is_visible()
        browser.close()
        return success
