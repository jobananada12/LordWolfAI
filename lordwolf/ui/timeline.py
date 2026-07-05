"""
LordWolf AI Studio

File:
lordwolf/ui/timeline.py

Version:
0.0.1

Purpose:
Панель таймлайну для відображення сцен мультфільму
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QLabel
)


class TimelinePanel(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.scenes = []

        self.init_ui()

    def init_ui(self):

        self.layout = QVBoxLayout(self)

        self.title = QLabel("🎬 Таймлайн")

        self.list_widget = QListWidget()

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.list_widget)

    def update_scenes(self, scenes):

        self.scenes = scenes

        self.list_widget.clear()

        if not scenes:

            self.list_widget.addItem("Немає сцен")

            return

        for scene in scenes:

            if hasattr(scene, "number"):

                title = getattr(scene, "title", "")
                self.list_widget.addItem(
                    f"Сцена {scene.number}: {title}"
                )

            else:

                self.list_widget.addItem(str(scene))

    def clear(self):
        self.scenes = []
        self.list_widget.clear()