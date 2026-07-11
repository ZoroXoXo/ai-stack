# may later load defaults from models/

#What it does: Centralizes runtime settings.
#Logic used: Config loading logic from env variables, JSON files, defaults, and path
#resolution.
#Interconnection: Almost every other runtime file depends on this, especially services and
#startup code

"""Central configuration for the laptop copilot.

Loads .env, resolves paths, and exposes a single Settings object. Nothing in
this module executes actions — it only describes where things live.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root if present. Safe to call multiple times.
_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(_ROOT / ".env")


def _env(key: str, default: str) -> str:
    return os.environ.get(key, default)


@dataclass
class Settings:
    root_dir: Path = _ROOT

    ollama_host: str = field(default_factory=lambda: _env("OLLAMA_HOST", "http://127.0.0.1:11434"))
    controller_model: str = field(default_factory=lambda: _env("CONTROLLER_MODEL", "none"))

    log_level: str = field(default_factory=lambda: _env("COPILOT_LOG_LEVEL", "INFO"))
    log_dir: Path = field(default_factory=lambda: _ROOT / _env("COPILOT_LOG_DIR", "./logs"))
    notes_dir: Path = field(default_factory=lambda: _ROOT / _env("COPILOT_NOTES_DIR", "./data/notes"))

    tools_config_path: Path = field(
        default_factory=lambda: _ROOT / _env("COPILOT_TOOLS_CONFIG", "./config/tools.json")
    )
    preferences_config_path: Path = field(
        default_factory=lambda: _ROOT / _env("COPILOT_PREFERENCES_CONFIG", "./config/preferences.json")
    )

    require_confirmation: bool = field(
        default_factory=lambda: _env("COPILOT_REQUIRE_CONFIRMATION", "true").lower() == "true"
    )

    def ensure_dirs(self) -> None:
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.notes_dir.mkdir(parents=True, exist_ok=True)

    def load_tools_config(self) -> dict:
        with open(self.tools_config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_preferences(self) -> dict:
        with open(self.preferences_config_path, "r", encoding="utf-8") as f:
            return json.load(f)


settings = Settings()