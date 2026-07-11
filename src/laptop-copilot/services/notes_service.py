#What it does: Manages note creation, reading, and organization.
#Logic used: File-based note persistence and retrieval logic.
#Interconnection: Writes into data/notes/, may connect to memory.py

"""Quick-note creation and retrieval."""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from laptop_copilot.config import settings


def _slugify(text: str, max_len: int = 40) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\-_]+", "-", text.strip().lower()).strip("-")
    return slug[:max_len] or "note"


def create_note(text: str, title: Optional[str] = None) -> Path:
    settings.ensure_dirs()
    ts = datetime.now()
    slug = _slugify(title or text)
    filename = f"{ts.strftime('%Y%m%d-%H%M%S')}-{slug}.md"
    path = settings.notes_dir / filename

    header = f"# {title or text.splitlines()[0][:60]}\n\n" if title else ""
    content = f"{header}{text}\n\n---\ncreated: {ts.isoformat()}\n"
    path.write_text(content, encoding="utf-8")
    return path


def list_notes(limit: int = 20) -> list[Path]:
    settings.ensure_dirs()
    notes = sorted(settings.notes_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return notes[:limit]