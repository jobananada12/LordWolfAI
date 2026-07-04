"""
LordWolf AI Studio

File:
lordwolf/ui/character_panel.py

Version:
0.0.1

Purpose:
Панель персонажів для відображення результатів Character AI
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QLabel
)


class CharacterPanel(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.characters = []

        self.init_ui()

    def init_ui(self):

        self.layout = QVBoxLayout(self)

        self.title = QLabel("🎭 Персонажі")
        self.list_widget = QListWidget()

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.list_widget)

    # 🔥 НОВИЙ МЕТОД ДЛЯ MAIN WINDOW
    def update_characters(self, characters):

        self.characters = characters

        self.list_widget.clear()

        if not characters:
            self.list_widget.addItem("Немає персонажів")
            return

        for char in characters:

            # підтримка як об'єкта, так і строки
            if hasattr(char, "name"):
                name = char.name
            else:
                name = str(char)

            self.list_widget.addItem(name)