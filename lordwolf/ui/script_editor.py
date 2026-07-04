from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel,
)
from PySide6.QtCore import Signal


class ScriptEditor(QWidget):
    """
    Редактор сценарію LordWolf AI Studio.
    """

    analyzeRequested = Signal(str)
    generateRequested = Signal(str)

    def __init__(self):
        super().__init__()

        self.build_ui()
        self.connect_signals()

    def build_ui(self):

        main_layout = QVBoxLayout()

        title = QLabel("📝 Редактор сценарію")
        title.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
        """)

        main_layout.addWidget(title)

        self.editor = QTextEdit()

        self.editor.setPlaceholderText(
"""Напишіть сценарій...

Приклад:

СЦЕНА 1

Вовк сидить біля великого каміна.

У двері стукають.

Заходить блондинка.

Вони починають розмову.
"""
        )

        main_layout.addWidget(self.editor)

        button_layout = QHBoxLayout()

        self.analyze_button = QPushButton("🔍 Аналізувати сценарій")
        self.generate_button = QPushButton("🎬 Створити мультфільм")
        self.clear_button = QPushButton("🗑 Очистити")

        button_layout.addWidget(self.analyze_button)
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)

        self.status = QLabel("Статус: Готовий до роботи.")

        self.status.setStyleSheet("""
            padding:6px;
            border:1px solid gray;
        """)

        main_layout.addWidget(self.status)

        self.setLayout(main_layout)

    def connect_signals(self):

        self.analyze_button.clicked.connect(self.analyze_script)

        self.generate_button.clicked.connect(self.generate_movie)

        self.clear_button.clicked.connect(self.editor.clear)

    def analyze_script(self):

        text = self.editor.toPlainText()

        self.status.setText("Статус: Аналіз сценарію...")

        self.analyzeRequested.emit(text)

    def generate_movie(self):

        text = self.editor.toPlainText()

        self.status.setText("Статус: Створення мультфільму...")

        self.generateRequested.emit(text)

    def get_script(self):

        return self.editor.toPlainText()

    def set_script(self, text):

        self.editor.setPlainText(text)

    def clear(self):

        self.editor.clear()

    def set_status(self, text):

        self.status.setText(f"Статус: {text}")