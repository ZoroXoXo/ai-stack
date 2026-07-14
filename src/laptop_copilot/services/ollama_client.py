#Will use selected model names at runtime from models/

#What it does: Talks to the Ollama API.
#Logic used: HTTP/API client logic for model listing, chat generation, health checks, and
#maybe embeddings.
#Interconnection: Uses settings from config.py and model choices from env/config/docs

"""Thin client for the local Ollama OpenAI-compatible API.

Only used if CONTROLLER_MODEL is set to something other than "none" — v1
routing is rule-based (see router.py) and does not require this at all.
Kept small on purpose: this is intent parsing, not a general chat client.
"""
from __future__ import annotations

import json
from typing import Optional

import httpx

from laptop_copilot.config import settings

INTENT_SCHEMA_PROMPT = """You are a strict intent parser for a desktop copilot.
Given a user request, respond with ONLY a JSON object of the form:
{"tool_name": "<one of: open_app, create_note, show_recent_files, open_last_file, open_calendar, show_clipboard, device_status>", "args": {...}}
No prose, no markdown, JSON only. If nothing matches, respond with:
{"tool_name": null, "args": {}}
"""


def parse_intent_with_model(request_text: str, model: Optional[str] = None) -> dict:
    """Ask the controller model to produce an intent dict. Caller is still
    responsible for validating the result against the tool whitelist —
    this function does not execute anything.
    """
    model = model or settings.controller_model
    if model in (None, "none", ""):
        raise RuntimeError("No controller model configured; use rule-based router instead.")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": INTENT_SCHEMA_PROMPT},
            {"role": "user", "content": request_text},
        ],
        "stream": False,
    }
    with httpx.Client(base_url=settings.ollama_host, timeout=15.0) as client:
        resp = client.post("/v1/chat/completions", json=payload)
        resp.raise_for_status()
        data = resp.json()

    content = data["choices"][0]["message"]["content"]
    cleaned = content.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(cleaned)