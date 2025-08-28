"""Credential storage using keyring."""
from __future__ import annotations

from typing import Tuple

import keyring


SERVICE_NAME = "VistaOrderAutomation"


def save_credentials(email: str, password: str) -> None:
    """Store credentials securely in the OS keyring."""
    keyring.set_password(SERVICE_NAME, "email", email)
    keyring.set_password(SERVICE_NAME, "password", password)


def load_credentials() -> Tuple[str, str]:
    """Retrieve stored credentials or empty strings if unavailable."""
    email = keyring.get_password(SERVICE_NAME, "email") or ""
    password = keyring.get_password(SERVICE_NAME, "password") or ""
    return email, password
