#Handles menu/launcher instructions

"""rofi integration: quick-access UI entry point and app launching.

The copilot's "wake" UI in v1 is a rofi prompt. This module also handles
resolving an app name to a launch command via `gtk-launch`/`.desktop`
lookup, falling back to a plain PATH lookup.
"""
from __future__ import annotations

import shutil
import subprocess
from typing import Optional


def prompt(message: str = "copilot") -> Optional[str]:
    """Show a rofi input prompt and return the typed text, or None if cancelled."""
    if shutil.which("rofi") is None:
        return None
    try:
        result = subprocess.run(
            ["rofi", "-dmenu", "-p", message],
            capture_output=True,
            text=True,
            timeout=30,
        )
        text = result.stdout.strip()
        return text or None
    except Exception:  # noqa: BLE001
        return None


def launch_app(app_name: str) -> tuple[bool, str]:
    """Launch an application by name, preferring desktop-file launch via gtk-launch."""
    app_name = app_name.strip()
    if not app_name:
        return False, "No application name given."

    if shutil.which("gtk-launch"):
        try:
            subprocess.Popen(
                ["gtk-launch", app_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True, f"Launched {app_name} via gtk-launch"
        except Exception:  # noqa: BLE001
            pass  # fall through to PATH lookup

    binary = shutil.which(app_name)
    if binary:
        subprocess.Popen([binary], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True, f"Launched {binary}"

    return False, f"Could not find an application or binary named '{app_name}'."