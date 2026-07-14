#sends desktop notifications 

"""Desktop notifications via notify-send, with a stdout fallback."""
from __future__ import annotations

import shutil
import subprocess


def notify(title: str, body: str = "") -> None:
    if shutil.which("notify-send"):
        subprocess.run(["notify-send", title, body], check=False)
    else:
        print(f"[copilot] {title}: {body}")