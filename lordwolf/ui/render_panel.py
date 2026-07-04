from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QProgressBar,
    QTextEdit
)
from PySide6.QtCore import Signal


class RenderPanel(QWidget):
    """
    Панель рендерингу мультфільму.
    """

    startRender = Signal()
    stopRender = Signal()

    def __init__(self):
        super().__init__()

        self.build_ui()
        self.connect_signals()

    def build_ui(self):

        layout = QVBoxLayout()

        title = QLabel("📹 Рендер мультфільму")
        title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        self.progress = QProgressBar()
        self.progress.setValue(0)

        layout.addWidget(self.progress)

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout.addWidget(self.log)

        self.render_button = QPushButton("▶ Почати рендер")
        self.stop_button = QPushButton("■ Зупинити")

        layout.addWidget(self.render_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def connect_signals(self):

        self.render_button.clicked.connect(self.startRender.emit)
        self.stop_button.clicked.connect(self.stopRender.emit)

    def add_log(self, text):

        self.log.append(text)

    def set_progress(self, value):

        self.progress.setValue(value)

    def clear_log(self):

        self.log.clear()