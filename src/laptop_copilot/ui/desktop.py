"""Desktop app shell: QMainWindow with a sidebar and stacked Copilot /
Research / Settings pages. This is the one-app shell described in the PRD's
productization milestone — a native Python UI now, with a clear path to a
Tauri-packaged version later without touching the underlying router/tools
logic.

Run with:
    python -m laptop_copilot.ui.desktop
or:
    ./scripts/run-desktop.sh
"""
from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from laptop_copilot.ui.pages.copilot_page import CopilotPage
from laptop_copilot.ui.pages.research_page import ResearchPage
from laptop_copilot.ui.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Stack")
        self.resize(1100, 700)

        root = QWidget()
        self.setCentralWidget(root)

        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 16, 16, 16)
        sidebar_layout.setSpacing(12)

        title = QLabel("AI Stack")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title.setStyleSheet("font-size: 16px; font-weight: 700;")
        sidebar_layout.addWidget(title)

        self.btn_copilot = QPushButton("Copilot")
        self.btn_research = QPushButton("Research")
        self.btn_settings = QPushButton("Settings")
        for b in (self.btn_copilot, self.btn_research, self.btn_settings):
            b.setCheckable(True)

        sidebar_layout.addWidget(self.btn_copilot)
        sidebar_layout.addWidget(self.btn_research)
        sidebar_layout.addWidget(self.btn_settings)
        sidebar_layout.addStretch()

        self.stack = QStackedWidget()
        self.page_copilot = CopilotPage()
        self.page_research = ResearchPage()
        self.page_settings = SettingsPage()

        self.stack.addWidget(self.page_copilot)
        self.stack.addWidget(self.page_research)
        self.stack.addWidget(self.page_settings)

        layout.addWidget(sidebar)
        layout.addWidget(self.stack)

        self.btn_copilot.clicked.connect(lambda: self._select(0))
        self.btn_research.clicked.connect(lambda: self._select(1))
        self.btn_settings.clicked.connect(lambda: self._select(2))
        self._select(0)

    def _select(self, index: int) -> None:
        self.stack.setCurrentIndex(index)
        for i, b in enumerate((self.btn_copilot, self.btn_research, self.btn_settings)):
            b.setChecked(i == index)


def run() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()