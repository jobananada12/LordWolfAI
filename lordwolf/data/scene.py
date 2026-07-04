"""
LordWolf AI Studio
Scene Data Model
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Scene:
    """
    Модель сцени мультфільму.

    Scene — це контейнер даних.
    Жодної AI-логіки тут бути не повинно.
    """

    number: int

    title: str

    actions: List[str] = field(default_factory=list)

    characters: List[str] = field(default_factory=list)

    backgrounds: List[str] = field(default_factory=list)

    animations: List[str] = field(default_factory=list)

    music: List[str] = field(default_factory=list)

    voices: List[str] = field(default_factory=list)

    camera: List[str] = field(default_factory=list)

    duration: float = 0.0

    notes: str = ""

    def add_action(self, action: str):

        if action:

            self.actions.append(action)

    def add_character(self, name: str):

        if name and name not in self.characters:

            self.characters.append(name)

    def add_background(self, name: str):

        if name and name not in self.backgrounds:

            self.backgrounds.append(name)

    def add_animation(self, animation: str):

        if animation and animation not in self.animations:

            self.animations.append(animation)

    def add_voice(self, voice: str):

        if voice and voice not in self.voices:

            self.voices.append(voice)

    def add_music(self, music: str):

        if music and music not in self.music:

            self.music.append(music)

    def add_camera(self, camera: str):

        if camera and camera not in self.camera:

            self.camera.append(camera)

    def clear(self):

        self.actions.clear()
        self.characters.clear()
        self.backgrounds.clear()
        self.animations.clear()
        self.music.clear()
        self.voices.clear()
        self.camera.clear()

        self.duration = 0.0

        self.notes = ""

    def __str__(self):

        return (
            f"Scene {self.number}: {self.title} "
            f"(Actions={len(self.actions)}, "
            f"Characters={len(self.characters)}, "
            f"Backgrounds={len(self.backgrounds)})"
        )