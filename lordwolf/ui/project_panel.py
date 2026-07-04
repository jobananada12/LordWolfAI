from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QHBoxLayout
)
from PySide6.QtCore import Signal


class ProjectPanel(QWidget):
    """
    Панель проєктів.
    """

    newProject = Signal()
    openProject = Signal()
    deleteProject = Signal(str)

    def __init__(self):
        super().__init__()

        self.build_ui()
        self.connect_signals()

    def build_ui(self):

        layout = QVBoxLayout()

        title = QLabel("📁 Проєкти")
        title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        self.project_list = QListWidget()

        layout.addWidget(self.project_list)

        buttons = QHBoxLayout()

        self.new_button = QPushButton("Новий")

        self.open_button = QPushButton("Відкрити")

        self.delete_button = QPushButton("Видалити")

        buttons.addWidget(self.new_button)
        buttons.addWidget(self.open_button)
        buttons.addWidget(self.delete_button)

        layout.addLayout(buttons)

        self.setLayout(layout)

    def connect_signals(self):

        self.new_button.clicked.connect(self.newProject.emit)

        self.open_button.clicked.connect(self.openProject.emit)

        self.delete_button.clicked.connect(self.delete_selected)

    def delete_selected(self):

        item = self.project_list.currentItem()

        if item is None:
            return

        self.deleteProject.emit(item.text())

    def add_project(self, name):

        self.project_list.addItem(name)

    def clear(self):

        self.project_list.clear()

    def current_project(self):

        item = self.project_list.currentItem()

        if item is None:
            return None

        return item.text()