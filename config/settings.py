"""Program configuration storage."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict

# Configuration stored in user's home directory
CONFIG_PATH = Path.home() / ".vista_order_settings.json"

# Default Crimpress login URL
DEFAULT_LOGIN_URL = (
    "https://cimpress.auth0.com/login?state=hKFo2SBhNDRLNG9wTnVKRHFsY2ZMaUZuWlNJWUNEV3lfRVVocKFupWxvZ2luo3RpZ"
    "NkgSUg0UW9abmQ1cmVXaHF5dWYyYjI5UUd6MXlkMDVnaXOjY2lk2SBKSk5XemRLSE9MNjhqZ2l2aDdMeVpXVU5PWFdVV2l0OQ&client=JJNWzdKHOL68jgivh7LyZWUNOXWUWit9&protocol=oauth2&responseType=id_token%20token&audience=https%3A%2F%2Fapi.cimpress.io%2F&scope=openid%20profile%20email%20user_id&redirect_uri=https%3A%2F%2Fpom.cimpress.io%2F&response_type=code&response_mode=query&nonce=M3FrNUVjMlNNNHJqQ1lzd3U3eHFCczVCOHk2SHMufkxIR0suVG1YaDVLeQ%3D%3D&code_challenge=JQjuE3t-CIHiQKdPyEFeM0Yn8UgaEoAA7PjKnT3k2Og&code_challenge_method=S256&auth0Client=eyJuYW1lIjoiYXV0aDAtc3BhLWpzIiwidmVyc2lvbiI6IjEuMjIuNiJ9"
)


def load_settings() -> Dict[str, str]:
    """Load stored settings or return defaults."""
    data: Dict[str, str] = {}
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text())
        except json.JSONDecodeError:
            data = {}

    if not data.get("login_url"):
        env_url = os.environ.get("CRIMPRESS_LOGIN_URL")
        data["login_url"] = env_url or DEFAULT_LOGIN_URL

    return data


def save_settings(art_root: str, login_url: str) -> None:
    """Persist program settings to disk."""
    data = {"art_root": art_root, "login_url": login_url}
    CONFIG_PATH.write_text(json.dumps(data))
