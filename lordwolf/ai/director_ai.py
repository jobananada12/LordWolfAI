"""
LordWolf AI Studio
Director AI
"""

from lordwolf.ai.script_ai import ScriptAI
from lordwolf.ai.character_ai import CharacterAI
from lordwolf.ai.background_ai import BackgroundAI
from lordwolf.ai.animation_ai import AnimationAI
from lordwolf.ai.voice_ai import VoiceAI

from lordwolf.data.project import MovieProject


class DirectorAI:
    """
    Головний координатор AI.

    Створює MovieProject,
    який потім передається всім Engines.
    """

    def __init__(self):

        self.script_ai = ScriptAI()

        self.character_ai = CharacterAI()

        self.background_ai = BackgroundAI()

        self.animation_ai = AnimationAI()

        self.voice_ai = VoiceAI()

        self.project = MovieProject()

    def create_movie(self, script):

        self.project.clear()

        self.project.script = script

        result = self.script_ai.analyze(script)

        self.project.scenes = result["scenes"]

        for name in result["characters"]:

            character = self.character_ai.create_character(name)

            self.project.characters.append(character)

        for name in result["backgrounds"]:

            background = self.background_ai.create_background(name)

            self.project.backgrounds.append(background)

        self.project.animations = self.animation_ai.get_all()

        self.project.voices = self.voice_ai.get_all()

        return self.project

    def get_movie_project(self):

        return self.project

    def reset(self):

        self.project.clear()

        self.character_ai.clear()

        self.background_ai.clear()