"""Settings page: live Ollama status/model list, plus a read-only view of
current preferences and the tool whitelist (config/*.json). Editing model
choice or preferences in v1 is done by hand in .env / config/*.json — this
page surfaces what's active rather than writing config, keeping the same
"predictable over clever" posture as the copilot router.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request

from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QFrame,
    QLabel,
    QListWidget,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from laptop_copilot.config import settings


class _OllamaStatusWorker(QThread):
    result = Signal(bool, list, str)  # ok, model_names, error_message

    def __init__(self, host: str, timeout: float = 3.0):
        super().__init__()
        self._host = host.rstrip("/")
        self._timeout = timeout

    def run(self) -> None:
        try:
            with urllib.request.urlopen(f"{self._host}/api/tags", timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            names = [m.get("name", "?") for m in data.get("models", [])]
            self.result.emit(True, names, "")
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            self.result.emit(False, [], str(e))
        except Exception as e:  # noqa: BLE001
            self.result.emit(False, [], f"Unexpected error: {e}")


class SettingsPage(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._worker: _OllamaStatusWorker | None = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(12)

        card = QFrame()
        card.setObjectName("card")
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 25))
        card.setGraphicsEffect(shadow)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(12)

        heading = QLabel("Settings")
        heading.setStyleSheet("font-size: 18px; font-weight: 600;")
        card_layout.addWidget(heading)

        card_layout.addWidget(QLabel(f"Ollama host: {settings.ollama_host}"))
        card_layout.addWidget(QLabel(f"Controller model: {settings.controller_model}"))
        card_layout.addWidget(QLabel(f"Confirm write actions: {settings.require_confirmation}"))

        self.check_btn = QPushButton("Check Ollama Status")
        self.check_btn.clicked.connect(self.check_ollama)
        self.check_btn.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.check_btn)

        self.status_label = QLabel("Status: not checked yet.")
        card_layout.addWidget(self.status_label)

        card_layout.addWidget(QLabel("Available models:"))
        self.model_list = QListWidget()
        self.model_list.setStyleSheet("border: 1px solid #d1d5db; border-radius: 14px;")
        card_layout.addWidget(self.model_list, stretch=1)

        card_layout.addWidget(QLabel("Whitelisted tools (config/tools.json):"))
        self.tools_view = QTextEdit()
        self.tools_view.setReadOnly(True)
        self.tools_view.setStyleSheet("background: #ffffff; border: 1px solid #d1d5db; border-radius: 14px; padding: 12px;")
        self._load_tools_config()
        card_layout.addWidget(self.tools_view, stretch=1)

        outer.addWidget(card, stretch=1)

    def _load_tools_config(self) -> None:
        try:
            cfg = settings.load_tools_config()
            lines = []
            for tool in cfg.get("tools", []):
                state = "enabled" if tool.get("enabled") else "disabled"
                write = " (write, confirms)" if tool.get("write") else ""
                lines.append(f"{tool['name']}: {state}{write} \u2014 {tool.get('description', '')}")
            self.tools_view.setPlainText("\n".join(lines))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.tools_view.setPlainText(f"Could not load config/tools.json: {e}")

    def check_ollama(self) -> None:
        self.status_label.setText("Checking\u2026")
        self.check_btn.setEnabled(False)
        self._worker = _OllamaStatusWorker(settings.ollama_host)
        self._worker.result.connect(self._on_result)
        self._worker.start()

    def _on_result(self, ok: bool, model_names: list[str], error_message: str) -> None:
        self.check_btn.setEnabled(True)
        self.model_list.clear()
        if ok:
            self.status_label.setText(f"Status: reachable \u2014 {len(model_names)} model(s) pulled.")
            self.model_list.addItems(model_names or ["(no models pulled yet)"])
        else:
            self.status_label.setText(f"Status: unreachable \u2014 {error_message}")