#What it does: Runs system commands safely.
#Logic used: Shell execution logic, probably with validation and output capture.
#Interconnection: Used by tools.py and maybe router.py for local automation tasks.


"""Runs a small, fixed set of OS-level commands.

This module never accepts raw shell strings from user or model text. Every
function here takes structured, already-validated arguments and builds an
argv list explicitly (no shell=True, no string interpolation into a shell).
"""
from __future__ import annotations

import shutil
import subprocess
from typing import Optional


def _run(argv: list[str]) -> tuple[bool, str]:
    if shutil.which(argv[0]) is None:
        return False, f"'{argv[0]}' not found on PATH"
    try:
        subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True, f"Launched: {' '.join(argv)}"
    except Exception as e:  # noqa: BLE001
        return False, f"Failed to launch {argv[0]}: {e}"


def open_path(path: str) -> tuple[bool, str]:
    """Open a file/path with the desktop default handler (xdg-open)."""
    return _run(["xdg-open", path])


def open_calendar() -> tuple[bool, str]:
    """Open a calendar application. Tries common candidates in order."""
    candidates = ["gnome-calendar", "korganizer", "thunderbird"]
    for app in candidates:
        if shutil.which(app):
            return _run([app])
    return False, "No known calendar application found on PATH."