#reads and writes clipboard content

"""Read-only clipboard access via xclip/wl-paste, whichever is present."""
from __future__ import annotations

import shutil
import subprocess
from typing import Optional


def read() -> Optional[str]:
    if shutil.which("wl-paste"):
        try:
            result = subprocess.run(["wl-paste"], capture_output=True, text=True, timeout=5)
            return result.stdout
        except Exception:  # noqa: BLE001
            return None
    if shutil.which("xclip"):
        try:
            result = subprocess.run(
                ["xclip", "-selection", "clipboard", "-o"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.stdout
        except Exception:  # noqa: BLE001
            return None
    return None