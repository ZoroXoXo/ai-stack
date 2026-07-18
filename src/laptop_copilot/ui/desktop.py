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

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QStyle,
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

        main_v = QVBoxLayout(root)
        main_v.setContentsMargins(0, 0, 0, 0)
        main_v.setSpacing(0)

        # Top header
        header = QFrame()
        header.setObjectName("topHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 12, 16, 12)
        header_layout.setSpacing(12)
        title_label = QLabel("AI Stack")
        title_label.setObjectName("appTitleSmall")
        title_label.setStyleSheet("color: #111827; font-weight: 700; font-size: 14px;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search the app — commands, settings, files")
        self.search.setClearButtonEnabled(True)
        self.search.setFixedWidth(360)
        header_layout.addWidget(self.search)

        # Content area (sidebar + stack)
        content = QWidget()
        layout = QHBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 16, 16, 16)
        sidebar_layout.setSpacing(12)

        title = QLabel("AI Stack")
        title.setObjectName("appTitle")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title.setStyleSheet("font-size: 16px; font-weight: 700;")
        sidebar_layout.addWidget(title)

        self.btn_copilot = QPushButton("Copilot")
        self.btn_research = QPushButton("Research")
        self.btn_settings = QPushButton("Settings")
        for b in (self.btn_copilot, self.btn_research, self.btn_settings):
            b.setCheckable(True)
            b.setCursor(Qt.PointingHandCursor)
            b.setMinimumHeight(44)
            b.setIconSize(QSize(18, 18))

        # set icons
        self.btn_copilot.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.btn_research.setIcon(self.style().standardIcon(QStyle.SP_DesktopIcon))
        self.btn_settings.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))

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
        self.stack.setContentsMargins(20, 20, 20, 20)

        # assemble main layout
        main_v.addWidget(header)
        main_v.addWidget(content)
        self.search.returnPressed.connect(self._on_search)
        self.btn_copilot.clicked.connect(lambda: self._select(0))
        self.btn_research.clicked.connect(lambda: self._select(1))
        self.btn_settings.clicked.connect(lambda: self._select(2))
        self._select(0)

    def _select(self, index: int) -> None:
        self.stack.setCurrentIndex(index)
        for i, b in enumerate((self.btn_copilot, self.btn_research, self.btn_settings)):
            b.setChecked(i == index)

    def _on_search(self) -> None:
        query = self.search.text().strip()
        if not query:
            return
        self.search.clear()
        self._select(0)
        self.page_copilot.run_request_text(query)


def run() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(
        """
        QWidget { background: #f5f7fb; color: #1f2937; font-family: Inter, 'Segoe UI', sans-serif; }
        QFrame#sidebar { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #111827, stop:1 #2563eb); }
        QLabel#appTitle { color: white; font-size: 18px; font-weight: 700; }
        QFrame#topHeader { background: transparent; }
        QLabel#appTitleSmall { color: #0f172a; }
        QPushButton { background: #ffffff; border: 1px solid #d1d5db; border-radius: 12px; padding: 10px 14px; min-height: 42px; }
        QFrame#sidebar QPushButton:checked { background: transparent; color: white; border: none; border-left: 4px solid #60a5fa; padding-left: 12px; }
        QFrame#sidebar QPushButton { background: transparent; color: rgba(255,255,255,0.9); border: none; text-align: left; padding: 10px 14px; }
        QFrame#sidebar QPushButton:hover { background: rgba(255,255,255,0.05); }
        QFrame#card { background: #ffffff; border: 1px solid rgba(15, 23, 42, 0.08); border-radius: 20px; }
        QPushButton:hover { background: #e2e8f0; }
        QPushButton:pressed { background: #c7d2fe; }
        QLineEdit, QTextEdit, QListWidget, QComboBox { background: #ffffff; border: 1px solid #d1d5db; border-radius: 12px; padding: 10px; }
        QLineEdit { background: #ffffff; }
        QLineEdit { min-height: 44px; }
        QTextEdit { border-radius: 14px; }
        QListWidget { border-radius: 14px; }
        QSplitter::handle { background: transparent; }
        QScrollBar:vertical { width: 10px; background: transparent; margin: 0px 0px 0px 0px; }
        QScrollBar::handle:vertical { background: #cbd5e1; border-radius: 5px; min-height: 20px; }
        QScrollBar::add-line, QScrollBar::sub-line { height: 0px; }
        QLabel { font-size: 13px; }
        """
    )
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()