from PySide6.QtWidgets import (
    QMainWindow,
    QDockWidget,
    QMessageBox,
    QFileDialog
)
from PySide6.QtCore import Qt
from pathlib import Path

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

        # ENGINE
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

        # Підключаємо рендер з панелі
        self.render_panel.startRender.connect(self.render_movie)

    # -----------------------------
    # UI ACTIONS
    # -----------------------------

    def new_project(self):

        Logger.info("New Project")

        # Очищаємо редактор
        self.script_editor.clear()
        self.script_editor.set_status("Новий проект створено")

        # Очищаємо панелі
        self.character_panel.clear()
        self.background_panel.clear()
        self.timeline_panel.clear()

        # Скидаємо двигун
        self.script_engine.reset()

        QMessageBox.information(
            self,
            APP_NAME,
            "✅ Новий проєкт створено!\n\n"
            "Можете починати писати сценарій."
        )

    def open_project(self):

        Logger.info("Open Project")

        # Відкриваємо діалог вибору файлу
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Відкрити проект",
            "projects",
            "LordWolf Project (*.wolf);;All Files (*.*)"
        )

        if file_path:
            QMessageBox.information(
                self,
                APP_NAME,
                f"📂 Відкрито проект: {Path(file_path).name}\n\n"
                "Функція завантаження проектів ще в розробці."
            )

    def save_project(self):

        Logger.info("Save Project")

        # Відкриваємо діалог збереження
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Зберегти проект",
            "projects/untitled.wolf",
            "LordWolf Project (*.wolf);;All Files (*.*)"
        )

        if file_path:
            QMessageBox.information(
                self,
                APP_NAME,
                f"💾 Проект збережено: {Path(file_path).name}\n\n"
                "Функція збереження проектів ще в розробці."
            )

    def generate_movie(self):

        Logger.info("Generate Movie")

        # Беремо текст з редактора
        script = self.script_editor.get_script()

        if not script.strip():
            QMessageBox.warning(
                self,
                APP_NAME,
                "⚠️ Сценарій порожній!\n\n"
                "Напишіть сценарій у редакторі."
            )
            return

        # Аналізуємо сценарій
        self.analyze_script(script)

        # Потім рендеримо відео
        self.render_movie()

    def show_settings(self):

        QMessageBox.information(
            self,
            APP_NAME,
            "⚙️ Налаштування\n\n"
            "Версія: " + VERSION + "\n"
            "Автор: " + AUTHOR + "\n\n"
            "Функція налаштувань ще в розробці."
        )

    # -----------------------------
    # MAIN PIPELINE
    # -----------------------------

    def analyze_script(self, script):

        Logger.info("Analyze Script")

        if not script.strip():
            QMessageBox.warning(
                self,
                APP_NAME,
                "⚠️ Сценарій порожній!\n\n"
                "Напишіть сценарій у редакторі."
            )
            return

        project = self.script_engine.process(script)

        # оновлення UI
        self.update_ui_from_project(project)

        # Показуємо результат
        self.script_editor.set_status(
            f"✅ Сценарій проаналізовано: {project.scene_count()} сцен, "
            f"{project.character_count()} персонажів, "
            f"{project.background_count()} фонів"
        )

        QMessageBox.information(
            self,
            APP_NAME,
            f"🎬 Проєкт створено!\n\n"
            f"📝 Сцен: {project.scene_count()}\n"
            f"🎭 Персонажів: {project.character_count()}\n"
            f"🌲 Фонів: {project.background_count()}\n"
            f"🎵 Озвучено: {len([v for s in project.scenes for v in s.voices])} реплік"
        )

    def generate_movie_from_script(self, script):

        Logger.info("Generate Movie From Script")

        self.analyze_script(script)
        self.render_movie()

    def render_movie(self):
        """
        Рендерить фінальне відео.
        """
        Logger.info("Початок рендерингу відео")

        # Перевіряємо, чи є проект
        if self.script_engine.last_project is None:
            QMessageBox.warning(
                self,
                APP_NAME,
                "⚠️ Спочатку проаналізуйте сценарій!\n\n"
                "Натисніть 'Аналізувати сценарій' або 'Створити мультфільм'."
            )
            return

        try:
            # Показуємо повідомлення про початок
            self.render_panel.add_log("🎬 Початок рендерингу...")
            self.render_panel.set_progress(10)

            # Рендеримо відео
            video_path = self.script_engine.director.render_movie("lordwolf_movie.mp4")

            self.render_panel.set_progress(90)

            if video_path:
                # Перевіряємо, чи файл існує
                if Path(video_path).exists():
                    file_size = Path(video_path).stat().st_size / 1024 / 1024
                    self.render_panel.add_log(f"✅ Відео створено: {video_path}")
                    self.render_panel.add_log(f"📊 Розмір: {file_size:.2f} MB")
                    self.render_panel.set_progress(100)

                    QMessageBox.information(
                        self,
                        APP_NAME,
                        f"🎉 Відео створено успішно!\n\n"
                        f"📁 Файл: {video_path}\n"
                        f"📊 Розмір: {file_size:.2f} MB"
                    )
                else:
                    self.render_panel.add_log("❌ Відео не створено")
                    QMessageBox.warning(
                        self,
                        APP_NAME,
                        "❌ Відео не створено.\n\n"
                        "Перевірте логи в терміналі."
                    )
            else:
                self.render_panel.add_log("❌ Помилка рендерингу")
                QMessageBox.warning(
                    self,
                    APP_NAME,
                    "❌ Не вдалося створити відео.\n\n"
                    "Перевірте:\n"
                    "1. Чи є зображення в assets/characters/\n"
                    "2. Чи є аудіо в audio_output/\n"
                    "3. Чи встановлено ffmpeg"
                )

        except Exception as e:
            Logger.error(f"Помилка рендерингу: {e}")
            self.render_panel.add_log(f"❌ Помилка: {str(e)}")
            QMessageBox.critical(
                self,
                APP_NAME,
                f"❌ Помилка рендерингу:\n\n{str(e)}"
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

        # Оновлюємо панель рендерингу
        self.render_panel.add_log(f"📝 Сцен: {len(scenes)}")
        self.render_panel.add_log(f"🎭 Персонажів: {len(characters)}")
        self.render_panel.add_log(f"🌲 Фонів: {len(backgrounds)}")
        self.render_panel.set_progress(0)

    def _safe_get(self, obj, key, default):

        """
        Підтримка dict і object одночасно
        """

        if obj is None:
            return default

        if isinstance(obj, dict):
            return obj.get(key, default)

        return getattr(obj, key, default)