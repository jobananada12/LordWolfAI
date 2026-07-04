from PySide6.QtWidgets import (
    QMainWindow,
    QDockWidget,
    QMessageBox
)
from PySide6.QtCore import Qt

from lordwolf.core.config import *
from lordwolf.core.logger import Logger

from lordwolf.engines.script_engine import ScriptEngine

from lordwolf.ui.toolbar import MainToolBar
from lordwolf.ui.script_editor import ScriptEditor
from lordwolf.ui.project_panel import ProjectPanel
from lordwolf.ui.character_panel import CharacterPanel
from lordwolf.ui.background_panel import BackgroundPanel
from lordwolf.ui.timeline import TimelinePanel
from lordwolf.ui.render_panel import RenderPanel


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        Logger.info("Starting Main Window")

        self.setWindowTitle(APP_NAME)

        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # 🔥 ENGINE
        self.script_engine = ScriptEngine()

        self.create_widgets()
        self.create_toolbar()
        self.create_layout()
        self.connect_signals()

    def create_widgets(self):

        self.script_editor = ScriptEditor()

        self.project_panel = ProjectPanel()

        self.character_panel = CharacterPanel()

        self.background_panel = BackgroundPanel()

        self.timeline_panel = TimelinePanel()

        self.render_panel = RenderPanel()

    def create_toolbar(self):

        self.toolbar = MainToolBar()

        self.addToolBar(self.toolbar)

    def create_layout(self):

        self.setCentralWidget(self.script_editor)

        # Проєкти
        project_dock = QDockWidget("📁 Проєкти", self)
        project_dock.setWidget(self.project_panel)
        self.addDockWidget(Qt.LeftDockWidgetArea, project_dock)

        # Персонажі
        character_dock = QDockWidget("🎭 Персонажі", self)
        character_dock.setWidget(self.character_panel)
        self.addDockWidget(Qt.RightDockWidgetArea, character_dock)

        # Фони
        background_dock = QDockWidget("🌲 Фони", self)
        background_dock.setWidget(self.background_panel)
        self.addDockWidget(Qt.RightDockWidgetArea, background_dock)

        self.tabifyDockWidget(character_dock, background_dock)

        # Таймлайн
        timeline_dock = QDockWidget("🎬 Таймлайн", self)
        timeline_dock.setWidget(self.timeline_panel)
        self.addDockWidget(Qt.BottomDockWidgetArea, timeline_dock)

        # Рендер
        render_dock = QDockWidget("📹 Рендер", self)
        render_dock.setWidget(self.render_panel)
        self.addDockWidget(Qt.BottomDockWidgetArea, render_dock)

        self.tabifyDockWidget(timeline_dock, render_dock)

    def connect_signals(self):

        self.toolbar.newProject.connect(self.new_project)
        self.toolbar.openProject.connect(self.open_project)
        self.toolbar.saveProject.connect(self.save_project)
        self.toolbar.generateMovie.connect(self.generate_movie)
        self.toolbar.settings.connect(self.show_settings)

        self.script_editor.analyzeRequested.connect(self.analyze_script)
        self.script_editor.generateRequested.connect(self.generate_movie_from_script)

    # -----------------------------
    # UI ACTIONS
    # -----------------------------

    def new_project(self):

        Logger.info("New Project")

        QMessageBox.information(
            self,
            APP_NAME,
            "Новий проєкт створено (поки що заглушка)"
        )

    def open_project(self):

        Logger.info("Open Project")

        QMessageBox.information(
            self,
            APP_NAME,
            "Відкрити проєкт (поки що заглушка)"
        )

    def save_project(self):

        Logger.info("Save Project")

        QMessageBox.information(
            self,
            APP_NAME,
            "Зберегти проєкт (поки що заглушка)"
        )

    def generate_movie(self):

        Logger.info("Generate Movie")

        QMessageBox.information(
            self,
            APP_NAME,
            "Генерація мультфільму (буде реалізовано далі)"
        )

    def show_settings(self):

        QMessageBox.information(
            self,
            APP_NAME,
            "Налаштування (поки що заглушка)"
        )

    # -----------------------------
    # MAIN PIPELINE
    # -----------------------------

    def analyze_script(self, script):

        Logger.info("Analyze Script")

        project = self.script_engine.process(script)

        # 🔥 оновлення UI
        self.update_ui_from_project(project)

        self.script_editor.set_status(
            "Сценарій проаналізовано і перетворено в проект"
        )

    def generate_movie_from_script(self, script):

        Logger.info("Generate Movie From Script")

        project = self.script_engine.process(script)

        self.update_ui_from_project(project)

        self.script_editor.set_status(
            "Проект готовий до генерації відео"
        )

    # -----------------------------
    # UI UPDATE ENGINE
    # -----------------------------

    def update_ui_from_project(self, project):

        # підтримка dict або object
        characters = self._safe_get(project, "characters", [])
        backgrounds = self._safe_get(project, "backgrounds", [])
        scenes = self._safe_get(project, "scenes", [])

        self.character_panel.update_characters(characters)
        self.background_panel.update_backgrounds(backgrounds)
        self.timeline_panel.update_scenes(scenes)

    def _safe_get(self, obj, key, default):

        """
        Підтримка dict і object одночасно
        """

        if obj is None:
            return default

        if isinstance(obj, dict):
            return obj.get(key, default)

        return getattr(obj, key, default)