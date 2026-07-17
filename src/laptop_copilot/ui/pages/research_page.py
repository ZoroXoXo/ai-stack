"""Research page: starts the Ollama + Open WebUI stack (scripts/run-research-ui.sh)
and opens it in the default browser. The research workspace itself is Open
WebUI running in the browser, not reimplemented in Qt — this page is just a
launcher/status surface, per the PRD's product split.
"""
from __future__ import annotations

import subprocess
import webbrowser
from typing import Optional

from PySide6.QtCore import QProcess
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget

from laptop_copilot.config import settings

import os


class ResearchPage(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._process: Optional[QProcess] = None
        self._port = os.environ.get("OPEN_WEBUI_PORT", "8080")

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

        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("Start Research Session")
        self.start_btn.clicked.connect(self.start_session)
        self.open_btn = QPushButton("Open in Browser")
        self.open_btn.clicked.connect(self.open_browser)
        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.open_btn)
        outer.addLayout(btn_row)

        self.status = QLabel("Not started.")
        outer.addWidget(self.status)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Startup output will appear here\u2026")
        outer.addWidget(self.log, stretch=1)

    def start_session(self) -> None:
        script = settings.root_dir / "scripts" / "run-research-ui.sh"
        if not script.exists():
            self.status.setText(f"Missing script: {script}")
            return

        self.status.setText("Starting Ollama + Open WebUI\u2026")
        self._process = QProcess(self)
        self._process.setProgram("bash")
        self._process.setArguments([str(script)])
        self._process.readyReadStandardOutput.connect(self._on_output)
        self._process.readyReadStandardError.connect(self._on_output)
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
        self.status.setText(f"Startup script finished. Open WebUI should be at http://localhost:{self._port}")

    def open_browser(self) -> None:
        webbrowser.open(f"http://localhost:{self._port}")