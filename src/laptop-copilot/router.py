#What it does: Decides where user requests should go.
#Logic used: Routing/orchestration logic; it inspects intent and decides whether to call tools,
#memory, model services, or UI actions.
#Interconnection: Likely sits between ui/cli.py and modules like tools.py, memory.py, and
#services/ollama_client.py

"""Maps natural-language requests to whitelisted tool intents.

v1 is rule/pattern based per the PRD ("predictable actions matter more than
generative fluency for desktop control"). If CONTROLLER_MODEL is set to
something other than "none" in .env, a small model can later be wired in
here to produce the same Intent contract — the rest of the system does not
need to change.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

from laptop_copilot import tools


@dataclass
class Intent:
    tool_name: str
    args: dict = field(default_factory=dict)
    confidence: float = 1.0


class UnroutableRequest(Exception):
    """Raised when no rule matches the request."""


# Ordered list of (regex, handler) — first match wins. Keep patterns narrow;
# a missed match should fall through to "I didn't understand," not to a
# wrong destructive action.
_PATTERNS: list[tuple[re.Pattern, callable]] = []


def _register(pattern: str):
    compiled = re.compile(pattern, re.IGNORECASE)

    def decorator(fn):
        _PATTERNS.append((compiled, fn))
        return fn

    return decorator


@_register(r"^open\s+(?:app|application)?\s*(.+)$")
def _route_open_app(m: re.Match) -> Intent:
    return Intent(tool_name="open_app", args={"app_name": m.group(1).strip()})


@_register(r"^(?:note|create note|new note)[:\s]+(.+)$")
def _route_create_note(m: re.Match) -> Intent:
    return Intent(tool_name="create_note", args={"text": m.group(1).strip()})


@_register(r"^(?:show\s+)?recent\s+files?(?:\s+(\d+))?$")
def _route_recent_files(m: re.Match) -> Intent:
    args = {}
    if m.group(1):
        args["limit"] = int(m.group(1))
    return Intent(tool_name="show_recent_files", args=args)


@_register(r"^open\s+(?:last|latest)\s+(?:file|download)$")
def _route_open_last_file(m: re.Match) -> Intent:
    return Intent(tool_name="open_last_file")


@_register(r"^(?:open\s+)?calendar$")
def _route_calendar(m: re.Match) -> Intent:
    return Intent(tool_name="open_calendar")


@_register(r"^(?:show\s+)?clipboard(?:\s+search\s+(.+))?$")
def _route_clipboard(m: re.Match) -> Intent:
    args = {}
    if m.group(1):
        args["query"] = m.group(1).strip()
    return Intent(tool_name="show_clipboard", args=args)


@_register(r"^(?:device\s+)?status$|^battery$|^network$")
def _route_status(m: re.Match) -> Intent:
    return Intent(tool_name="device_status")


def route(request_text: str) -> Intent:
    """Parse free text into an Intent. Raises UnroutableRequest if nothing matches."""
    text = request_text.strip()
    for pattern, handler in _PATTERNS:
        match = pattern.match(text)
        if match:
            intent = handler(match)
            if tools.get_tool(intent.tool_name) is None:
                # Defensive: a pattern referenced a tool that isn't registered.
                raise UnroutableRequest(f"Matched pattern but tool '{intent.tool_name}' is not registered.")
            return intent
    raise UnroutableRequest(f"Could not match request to a known action: {request_text!r}")