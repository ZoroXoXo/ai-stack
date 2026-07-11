#What it does: Displays runtime state or health information.
#Logic used: Status rendering logic.
#Interconnection: Reads from config/services and shows state to the user.

"""Formats ToolResult objects into human-readable feedback for the CLI/UI."""
from __future__ import annotations

from laptop_copilot.tools import ToolResult


def format_result(tool_name: str, result: ToolResult) -> str:
    icon = "✓" if result.ok else "✗"
    lines = [f"{icon} {tool_name}: {result.message}"]

    if result.data:
        if "files" in result.data:
            for f in result.data["files"][:10]:
                lines.append(f"    {f['path']}")
        elif "contents" in result.data:
            preview = (result.data["contents"] or "").strip().replace("\n", " ")[:200]
            lines.append(f"    {preview}")
        elif "battery" in result.data or "network" in result.data:
            batt = result.data.get("battery", {})
            net = result.data.get("network", {})
            if batt.get("available"):
                lines.append(f"    Battery: {batt['percent']}% ({batt['status']})")
            if net.get("connected"):
                lines.append(f"    Network: connected to {net.get('ssid', '?')}")
            elif net.get("connected") is False:
                lines.append("    Network: not connected")

    return "\n".join(lines)