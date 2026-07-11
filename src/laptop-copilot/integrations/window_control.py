#controls windows or focus behavior

"""Read-only device status: battery and network. No window-manipulation
actions are implemented in v1 — this module is a placeholder for future,
carefully-scoped window control (e.g. focus/workspace switch), which should
stay read-only or narrowly whitelisted if ever added.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any


def _battery_status() -> dict[str, Any]:
    bat_dirs = sorted(Path("/sys/class/power_supply").glob("BAT*")) if Path("/sys/class/power_supply").exists() else []
    if not bat_dirs:
        return {"available": False}
    bat = bat_dirs[0]
    try:
        capacity = (bat / "capacity").read_text().strip()
        status = (bat / "status").read_text().strip()
        return {"available": True, "percent": int(capacity), "status": status}
    except Exception:  # noqa: BLE001
        return {"available": False}


def _network_status() -> dict[str, Any]:
    if shutil.which("nmcli"):
        try:
            result = subprocess.run(
                ["nmcli", "-t", "-f", "ACTIVE,SSID", "dev", "wifi"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            active_lines = [line for line in result.stdout.splitlines() if line.startswith("yes:")]
            if active_lines:
                ssid = active_lines[0].split(":", 1)[1]
                return {"connected": True, "ssid": ssid}
            return {"connected": False}
        except Exception:  # noqa: BLE001
            return {"connected": None, "error": "nmcli query failed"}
    return {"connected": None, "error": "nmcli not found"}


def device_status() -> dict[str, Any]:
    return {"battery": _battery_status(), "network": _network_status()}