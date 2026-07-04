"""
LordWolf AI Studio
Script Engine
"""

from typing import Optional

from lordwolf.ai.director_ai import DirectorAI
from lordwolf.data.project import MovieProject


class ScriptEngine:
    """
    Script Engine

    Вхідна точка всієї AI системи.

    Отримує сценарій від UI,
    передає його DirectorAI,
    повертає готовий MovieProject.
    """

    def __init__(self):

        self.director = DirectorAI()

        self.last_project: Optional[MovieProject] = None

    # -------------------------------------------------
    # MAIN
    # -------------------------------------------------

    def process(self, script: str) -> MovieProject:
        """
        Побудова MovieProject із текстового сценарію.
        """

        self.last_project = self.director.create_movie(script)

        return self.last_project

    # -------------------------------------------------
    # ACCESS
    # -------------------------------------------------

    def get_movie_project(self) -> Optional[MovieProject]:

        return self.last_project

    def has_project(self) -> bool:

        return self.last_project is not None

    def get_scenes(self):

        if not self.has_project():
            return []

        return self.last_project.scenes

    def get_characters(self):

        if not self.has_project():
            return []

        return self.last_project.characters

    def get_backgrounds(self):

        if not self.has_project():
            return []

        return self.last_project.backgrounds

    # -------------------------------------------------
    # RESET
    # -------------------------------------------------

    def reset(self):

        self.last_project = None

        self.director.reset()