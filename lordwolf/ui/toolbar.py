from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal


class MainToolBar(QToolBar):
    """
    Головна панель інструментів LordWolf AI Studio
    """

    newProject = Signal()
    openProject = Signal()
    saveProject = Signal()
    generateMovie = Signal()
    settings = Signal()

    def __init__(self):
        super().__init__("Головна панель")

        self.build_toolbar()

    def build_toolbar(self):

        self.setMovable(False)

        action_new = QAction("📁 Новий", self)
        action_open = QAction("📂 Відкрити", self)
        action_save = QAction("💾 Зберегти", self)
        action_generate = QAction("🎬 Створити", self)
        action_settings = QAction("⚙ Налаштування", self)

        self.addAction(action_new)
        self.addSeparator()

        self.addAction(action_open)
        self.addSeparator()

        self.addAction(action_save)
        self.addSeparator()

        self.addAction(action_generate)
        self.addSeparator()

        self.addAction(action_settings)

        action_new.triggered.connect(self.newProject.emit)
        action_open.triggered.connect(self.openProject.emit)
        action_save.triggered.connect(self.saveProject.emit)
        action_generate.triggered.connect(self.generateMovie.emit)
        action_settings.triggered.connect(self.settings.emit)