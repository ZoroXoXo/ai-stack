#What it does: Stores and retrieves user or workspace memory.
#Logic used: Memory retrieval and persistence logic, such as saving notes, summaries, or
#context.
#Interconnection: Uses data/memory/, may rely on notes_service.py, and is probably
#triggered through router.py

"""Persistent action history/log for transparency and debugging.

Appends one JSON line per action to logs/actions.jsonl. Deliberately simple
(JSONL, not a database) so it's easy to tail, grep, and inspect by hand.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from laptop_copilot.config import settings


def _log_path() -> Path:
    settings.ensure_dirs()
    return settings.log_dir / "actions.jsonl"


def log_action(
    tool_name: str,
    args: dict,
    ok: bool,
    message: str,
    confirmed: Optional[bool] = None,
) -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": tool_name,
        "args": args,
        "ok": ok,
        "message": message,
        "confirmed": confirmed,
    }
    with open(_log_path(), "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def recent_actions(limit: int = 20) -> list[dict[str, Any]]:
    path = _log_path()
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    entries = [json.loads(line) for line in lines[-limit:]]
    return list(reversed(entries))