"""Program configuration storage."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

# Configuration stored in user's home directory
CONFIG_PATH = Path.home() / ".vista_order_settings.json"


def load_settings() -> Dict[str, str]:
    """Load stored settings or return defaults."""
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_settings(art_root: str) -> None:
    """Persist program settings to disk."""
    data = {"art_root": art_root}
    CONFIG_PATH.write_text(json.dumps(data))
