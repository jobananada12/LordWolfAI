"""
LordWolf AI Studio

File:
lordwolf/ui/background_panel.py

Version:
0.0.1

Purpose:
Панель фонів для відображення результатів Background AI
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QLabel
)


class BackgroundPanel(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.backgrounds = []

        self.init_ui()

    def init_ui(self):

        self.layout = QVBoxLayout(self)

        self.title = QLabel("🌲 Фони")

        self.list_widget = QListWidget()

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.list_widget)

    def update_backgrounds(self, backgrounds):

        self.backgrounds = backgrounds

        self.list_widget.clear()

        if not backgrounds:

            self.list_widget.addItem("Немає фонів")

            return

        for background in backgrounds:

            if hasattr(background, "name"):

                name = background.name

            else:

                name = str(background)

            self.list_widget.addItem(name)