#!/usr/bin/env python3
"""Retrieve an access token for Cimpress APIs via Auth0 client-credentials."""

from __future__ import annotations

import datetime as _dt
import os
import sys
from typing import Any, Dict

import requests

TOKEN_URL = "https://cimpress.auth0.com/oauth/token"
AUDIENCE = "https://api.cimpress.io/"
TIMEOUT = 30


class TokenRequestError(RuntimeError):
    """Raised when the Auth0 token endpoint returns an error."""


class MissingEnvironmentError(RuntimeError):
    """Raised when required environment variables are not present."""


def _read_env() -> Dict[str, str]:
    client_id = os.environ.get("CIMPRESS_CLIENT_ID")
    client_secret = os.environ.get("CIMPRESS_CLIENT_SECRET")

    missing = [
        name
        for name, value in (
            ("CIMPRESS_CLIENT_ID", client_id),
            ("CIMPRESS_CLIENT_SECRET", client_secret),
        )
        if not value
    ]
    if missing:
        raise MissingEnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    return {"client_id": client_id, "client_secret": client_secret}  # type: ignore[arg-type]


def request_token(client_id: str, client_secret: str) -> Dict[str, Any]:
    """Request an access token using the client-credentials grant."""

    payload = {
        "grant_type": "client_credentials",
        "audience": AUDIENCE,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(TOKEN_URL, json=payload, timeout=TIMEOUT)

    try:
        data = response.json()
    except ValueError as exc:  # pragma: no cover - safeguard for unexpected responses
        response.raise_for_status()
        raise TokenRequestError("Token endpoint returned non-JSON response") from exc

    if not response.ok:
        error = data.get("error", "unknown_error")
        description = data.get("error_description") or data
        raise TokenRequestError(f"Token request failed: {error}: {description}")

    return data


def main() -> None:
    credentials = _read_env()
    token_data = request_token(**credentials)

    access_token = token_data["access_token"]
    expires_in = int(token_data.get("expires_in", 0))
    expires_at = _dt.datetime.utcnow() + _dt.timedelta(seconds=expires_in)

    print(f"Access token: {access_token}")
    print(f"Expires in: {expires_in} seconds")
    print(f"Expires at (UTC): {expires_at.isoformat(timespec='seconds')}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover - allow propagation after logging
        print(f"Error: {exc}", file=sys.stderr)
        raise
