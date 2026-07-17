"""Copilot page: the same router -> tools -> memory pipeline used by the
CLI (see laptop_copilot.ui.cli), wired into a Qt widget instead of a
terminal prompt. No new capabilities are added here — this page can only
do what the CLI can already do, via the same whitelist.
"""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from laptop_copilot import memory, router, tools
from laptop_copilot.config import settings
from laptop_copilot.ui.status import format_result


class CopilotPage(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        settings.ensure_dirs()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(12)

        heading = QLabel("Copilot")
        heading.setStyleSheet("font-size: 18px; font-weight: 600;")
        outer.addWidget(heading)

        hint = QLabel(
            "Try: \u201copen firefox\u201d \u00b7 \u201cnote: buy milk\u201d \u00b7 "
            "\u201crecent files\u201d \u00b7 \u201ccalendar\u201d \u00b7 \u201cclipboard\u201d \u00b7 \u201cbattery\u201d"
        )
        hint.setWordWrap(True)
        hint.setStyleSheet("color: gray;")
        outer.addWidget(hint)

        input_row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a request and press Enter\u2026")
        self.input.returnPressed.connect(self.run_request)
        run_btn = QPushButton("Run")
        run_btn.clicked.connect(self.run_request)
        input_row.addWidget(self.input)
        input_row.addWidget(run_btn)
        outer.addLayout(input_row)

        splitter = QSplitter(Qt.Horizontal)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Output will appear here\u2026")
        splitter.addWidget(self.output)

        history_container = QWidget()
        history_layout = QVBoxLayout(history_container)
        history_layout.setContentsMargins(0, 0, 0, 0)
        history_label = QLabel("Recent actions")
        history_label.setStyleSheet("font-weight: 600;")
        self.history_list = QListWidget()
        history_layout.addWidget(history_label)
        history_layout.addWidget(self.history_list)
        splitter.addWidget(history_container)

        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        outer.addWidget(splitter, stretch=1)

        self.refresh_history()

    def append_output(self, text: str) -> None:
        self.output.append(text)
        self.output.append("")  # spacer

    def refresh_history(self) -> None:
        self.history_list.clear()
        for entry in memory.recent_actions(limit=20):
            icon = "\u2713" if entry["ok"] else "\u2717"
            self.history_list.addItem(f"{icon} {entry['tool']} \u2014 {entry['message']}")

    def run_request(self) -> None:
        text = self.input.text().strip()
        if not text:
            return
        self.input.clear()

        try:
            intent = router.route(text)
        except router.UnroutableRequest:
            self.append_output(
                f"\u2717 Didn't understand: {text!r}\n"
                f"Known actions: {', '.join(tools.list_tools())}"
            )
            return

        tool = tools.get_tool(intent.tool_name)
        if tool is None:
            self.append_output(f"\u2717 Internal error: unknown tool '{intent.tool_name}'")
            return

        confirmed = None
        if tool.write and settings.require_confirmation:
            reply = QMessageBox.question(
                self,
                "Confirm action",
                f"Run '{tool.name}' with {intent.args}?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            confirmed = reply == QMessageBox.Yes
            if not confirmed:
                memory.log_action(tool.name, intent.args, ok=False, message="Cancelled by user", confirmed=False)
                self.append_output(f"Cancelled: {tool.name}")
                self.refresh_history()
                return

        result = tool.handler(**intent.args)
        self.append_output(format_result(tool.name, result))
        memory.log_action(tool.name, intent.args, ok=result.ok, message=result.message, confirmed=confirmed)
        self.refresh_history()