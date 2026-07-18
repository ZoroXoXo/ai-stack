"""Research page: starts the Ollama + Open WebUI stack (scripts/run-research-ui.sh)
and embeds it inside the desktop app. This page launches the research stack
and shows the Open WebUI workspace through an integrated browser view.
"""
from __future__ import annotations

from typing import Optional

import os

from PySide6.QtCore import QProcess, QUrl, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from laptop_copilot.config import settings


class ResearchPage(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._process: Optional[QProcess] = None
        self.webview: QWebEngineView | None = None
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

        heading = QLabel("Research")
        heading.setStyleSheet("font-size: 18px; font-weight: 600;")
        card_layout.addWidget(heading)

        desc = QLabel(
            "The research workspace runs as Open WebUI, backed by local Ollama "
            "models. Starting it launches both and loads the workspace directly "
            "inside the app."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: gray;")
        card_layout.addWidget(desc)

        self.model_label = QLabel(
            f"Model: {os.environ.get('RESEARCH_MODEL', 'phi3.5:3.8b-mini-instruct-q4_K_M')}"
        )
        self.model_label.setStyleSheet("font-style: italic; color: gray;")
        card_layout.addWidget(self.model_label)

        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("Start Research Session")
        self.start_btn.clicked.connect(self.start_session)
        self.open_btn = QPushButton("Load Research Workspace")
        self.open_btn.clicked.connect(self.open_browser)
        self.open_btn.setEnabled(False)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.open_btn.setCursor(Qt.PointingHandCursor)
        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.open_btn)
        card_layout.addLayout(btn_row)

        self.status = QLabel("Not started.")
        card_layout.addWidget(self.status)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Startup output will appear here\u2026")
        self.log.setStyleSheet("background: #ffffff; border: 1px solid #d1d5db; border-radius: 14px; padding: 14px;")
        card_layout.addWidget(self.log, stretch=1)

        outer.addWidget(card, stretch=1)

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
        self.status.setText("Startup script finished. Research workspace is available inside the app.")
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
        if self.webview is None:
            try:
                from PySide6.QtWebEngineWidgets import QWebEngineView
            except Exception as exc:
                self.status.setText(f"Unable to load embedded browser: {exc}")
                return

            self.webview = QWebEngineView()
            self.webview.setMinimumHeight(420)
            self.webview.setStyleSheet("border: 1px solid #d1d5db; border-radius: 20px; background: #ffffff;")
            self.layout().addWidget(self.webview, stretch=2)

        self.webview.setVisible(True)
        self.webview.setUrl(QUrl(self._url))
        self.status.setText("Research workspace loaded inside the app.")