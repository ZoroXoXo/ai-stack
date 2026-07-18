"""Research page: starts the Ollama + Open WebUI stack (scripts/run-research-ui.sh)
and opens it in the default browser. The research workspace itself is Open
WebUI running in the browser, not reimplemented in Qt — this page is just a
launcher/status surface, per the PRD's product split.
"""
from __future__ import annotations

import subprocess
import webbrowser
from typing import Optional

from PySide6.QtCore import QProcess, Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget

from laptop_copilot.config import settings

import os


class ResearchPage(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._process: Optional[QProcess] = None
        # Prefer an explicit FRONTEND_URL (e.g. http://localhost:3000).
        # Fall back to OPEN_WEBUI_PORT (default 3000) for local Open WebUI installs.
        self._frontend_url = os.environ.get("FRONTEND_URL")
        if self._frontend_url:
            self._url = self._frontend_url
        else:
            self._url = f"http://localhost:{os.environ.get('OPEN_WEBUI_PORT', '3000')}"

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(12)

        heading = QLabel("Research")
        heading.setStyleSheet("font-size: 18px; font-weight: 600;")
        outer.addWidget(heading)

        desc = QLabel(
            "The research workspace runs as Open WebUI, backed by local Ollama "
            "models. Starting it launches both and opens the workspace in your "
            "browser."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: gray;")
        outer.addWidget(desc)

        self.model_label = QLabel(
            f"Model: {os.environ.get('RESEARCH_MODEL', 'phi3.5:3.8b-mini-instruct-q4_K_M')}"
        )
        self.model_label.setStyleSheet("font-style: italic; color: gray;")
        outer.addWidget(self.model_label)

        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("Start Research Session")
        self.start_btn.clicked.connect(self.start_session)
        self.open_btn = QPushButton("Open in Browser")
        self.open_btn.clicked.connect(self.open_browser)
        self.open_btn.setEnabled(False)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.open_btn.setCursor(Qt.PointingHandCursor)
        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.open_btn)
        outer.addLayout(btn_row)

        self.status = QLabel("Not started.")
        outer.addWidget(self.status)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Startup output will appear here\u2026")
        self.log.setStyleSheet("background: #ffffff; border: 1px solid #d1d5db; border-radius: 14px; padding: 14px;")
        outer.addWidget(self.log, stretch=1)

    def start_session(self) -> None:
        script = settings.root_dir / "scripts" / "run-research-ui.sh"
        if not script.exists():
            self.status.setText(f"Missing script: {script}")
            return

        self.status.setText("Starting Ollama + Open WebUI…")
        self.start_btn.setEnabled(False)
        self.open_btn.setEnabled(False)
        self._process = QProcess(self)
        self._process.setProgram("bash")
        self._process.setArguments([str(script)])
        self._process.readyReadStandardOutput.connect(self._on_output)
        self._process.readyReadStandardError.connect(self._on_output)
        self._process.errorOccurred.connect(self._on_error)
        self._process.finished.connect(self._on_finished)
        self._process.start()

    def _on_output(self) -> None:
        if self._process is None:
            return
        out = bytes(self._process.readAllStandardOutput()).decode(errors="replace")
        err = bytes(self._process.readAllStandardError()).decode(errors="replace")
        if out:
            self.log.append(out.strip())
        if err:
            self.log.append(err.strip())

    def _on_finished(self) -> None:
        self.status.setText(f"Startup script finished. Open WebUI should be at {self._url}")
        try:
            self.open_btn.setEnabled(True)
            self.start_btn.setEnabled(True)
        except Exception:
            pass

    def _on_error(self) -> None:
        self.status.setText("Failed to start research session. See logs for details.")
        try:
            self.open_btn.setEnabled(False)
            self.start_btn.setEnabled(True)
        except Exception:
            pass
        if self._process is not None:
            error_text = bytes(self._process.readAllStandardError()).decode(errors="replace").strip()
            if error_text:
                self.log.append(error_text)

    def open_browser(self) -> None:
        webbrowser.open(self._url)