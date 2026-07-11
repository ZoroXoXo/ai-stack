#What it does: Handles file operations.
#Logic used: File read/write/search/list logic.
#Interconnection: Likely used by tools, notes, and memory-related workflows


"""Recent-file lookup across common user directories (read-only)."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

# Directories scanned for "recent files." Kept explicit and small — this is
# not a general filesystem crawler.
_WATCHED_DIRS = [
    Path.home() / "Downloads",
    Path.home() / "Documents",
    Path.home() / "Desktop",
]


def recent_files(limit: int = 10) -> list[dict[str, Any]]:
    candidates: list[tuple[float, Path]] = []
    for d in _WATCHED_DIRS:
        if not d.exists():
            continue
        for entry in d.iterdir():
            if entry.is_file():
                try:
                    mtime = entry.stat().st_mtime
                except OSError:
                    continue
                candidates.append((mtime, entry))

    candidates.sort(key=lambda t: t[0], reverse=True)
    top = candidates[:limit]
    return [{"path": str(p), "modified": mtime} for mtime, p in top]