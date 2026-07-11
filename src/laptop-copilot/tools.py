#What it does: Defines actionable capabilities the copilot can perform.
#Logic used: Tool-execution logic, such as file tasks, system commands, or note operations.
#Interconnection: Probably calls services/command_runner.py, services/file_service.py,
#and integrations like clipboard or notifications.

"""The tool whitelist.

This is the single point through which the copilot is allowed to touch the
system. Router intents are mapped to a `Tool` here; nothing outside this
registry can be invoked, and no tool accepts raw shell strings from
user/model text. Each tool's `handler` receives already-validated,
schema-checked arguments only.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from laptop_copilot.services import command_runner, file_service, notes_service
from laptop_copilot.integrations import clipboard, notifications, rofi, window_control


@dataclass
class Tool:
    name: str
    description: str
    handler: Callable[..., "ToolResult"]
    args_schema: dict = field(default_factory=dict)  # {arg_name: type_name}
    write: bool = False  # True => destructive/modifying, may require confirmation
    read_only: bool = True


@dataclass
class ToolResult:
    ok: bool
    message: str
    data: Optional[dict] = None


def _open_application(app_name: str) -> ToolResult:
    ok, msg = rofi.launch_app(app_name)
    return ToolResult(ok=ok, message=msg)


def _create_note(text: str, title: Optional[str] = None) -> ToolResult:
    path = notes_service.create_note(text=text, title=title)
    notifications.notify("Note saved", str(path))
    return ToolResult(ok=True, message=f"Note saved to {path}", data={"path": str(path)})


def _show_recent_files(limit: int = 10) -> ToolResult:
    files = file_service.recent_files(limit=limit)
    return ToolResult(ok=True, message=f"Found {len(files)} recent files", data={"files": files})


def _open_last_file() -> ToolResult:
    files = file_service.recent_files(limit=1)
    if not files:
        return ToolResult(ok=False, message="No recent files found")
    ok, msg = command_runner.open_path(files[0]["path"])
    return ToolResult(ok=ok, message=msg, data={"path": files[0]["path"]})

def _open_calendar() -> ToolResult:
    ok, msg = command_runner.open_calendar()
    return ToolResult(ok=ok, message=msg)


def _show_clipboard(query: Optional[str] = None) -> ToolResult:
    contents = clipboard.read()
    if query:
        match = query.lower() in (contents or "").lower()
        return ToolResult(ok=True, message="Match found" if match else "No match", data={"contents": contents, "match": match})
    return ToolResult(ok=True, message="Clipboard read", data={"contents": contents})


def _device_status() -> ToolResult:
    status = window_control.device_status()
    return ToolResult(ok=True, message="Device status retrieved", data=status)


# The whitelist. This dict is the ONLY way an intent becomes an action.
REGISTRY: dict[str, Tool] = {
    "open_app": Tool(
        name="open_app",
        description="Launch an installed application by name.",
        handler=_open_application,
        args_schema={"app_name": "str"},
        write=False,
        read_only=False,  # launches a process, but not destructive
    ),
    "create_note": Tool(
        name="create_note",
        description="Create a quick note in the notes directory.",
        handler=_create_note,
        args_schema={"text": "str", "title": "str?"},
        write=True,
        read_only=False,
    ),
    "show_recent_files": Tool(
        name="show_recent_files",
        description="List recently modified/opened files.",
        handler=_show_recent_files,
        args_schema={"limit": "int?"},
        write=False,
        read_only=True,
    ),
    "open_last_file": Tool(
        name="open_last_file",
        description="Open the most recently used/downloaded file.",
        handler=_open_last_file,
        args_schema={},
        write=False,
        read_only=False,
    ),
    "open_calendar": Tool(
        name="open_calendar",
        description="Open the calendar application or a read-only calendar view.",
        handler=_open_calendar,
        args_schema={},
        write=False,
        read_only=True,
    ),
    "show_clipboard": Tool(
        name="show_clipboard",
        description="Show current clipboard contents, or search it for a query string.",
        handler=_show_clipboard,
        args_schema={"query": "str?"},
        write=False,
        read_only=True,
    ),
    "device_status": Tool(
        name="device_status",
        description="Show battery and network status.",
        handler=_device_status,
        args_schema={},
        write=False,
        read_only=True,
    ),
}


def get_tool(name: str) -> Optional[Tool]:
    return REGISTRY.get(name)


def list_tools() -> list[str]:
    return sorted(REGISTRY.keys())