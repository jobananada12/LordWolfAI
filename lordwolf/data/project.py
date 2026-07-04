"""
LordWolf AI Studio
Movie Project (CORE v2)
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any


# -----------------------------
# SCENE
# -----------------------------
@dataclass
class Scene:

    number: int
    title: str

    actions: List[str] = field(default_factory=list)

    characters: List[str] = field(default_factory=list)
    backgrounds: List[str] = field(default_factory=list)
    animations: List[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


# -----------------------------
# CHARACTER
# -----------------------------
@dataclass
class CharacterRef:

    name: str
    role: str = "unknown"
    description: str = ""

    def to_dict(self):
        return asdict(self)


# -----------------------------
# BACKGROUND
# -----------------------------
@dataclass
class BackgroundRef:

    name: str
    category: str = "unknown"
    description: str = ""

    def to_dict(self):
        return asdict(self)


# -----------------------------
# MOVIE PROJECT
# -----------------------------
class MovieProject:
    """
    Центральний контейнер всієї AI системи.
    """

    def __init__(self):

        self.title = "Новий проєкт"
        self.script = ""

        self.scenes: List[Scene] = []
        self.characters: List[CharacterRef] = []
        self.backgrounds: List[BackgroundRef] = []

        self.animations: List[Any] = []
        self.voices: List[Any] = []
        self.music: List[Any] = []
        self.camera: List[Any] = []

        self.render_settings: Dict[str, Any] = {}

    # -------------------------
    # RESET
    # -------------------------
    def clear(self):

        self.__init__()

    # -------------------------
    # COUNTERS
    # -------------------------
    def scene_count(self):
        return len(self.scenes)

    def character_count(self):
        return len(self.characters)

    def background_count(self):
        return len(self.backgrounds)

    # -------------------------
    # SERIALIZATION SAFE
    # -------------------------
    def to_dict(self):

        return {
            "title": self.title,
            "script": self.script,

            "scene_count": self.scene_count(),
            "character_count": self.character_count(),
            "background_count": self.background_count(),

            "scenes": [s.to_dict() for s in self.scenes],
            "characters": [c.to_dict() for c in self.characters],
            "backgrounds": [b.to_dict() for b in self.backgrounds],

            "animations": self.animations,
            "voices": self.voices,
            "music": self.music,
            "camera": self.camera,

            "render_settings": self.render_settings
        }

    # -------------------------
    # DEBUG
    # -------------------------
    def __str__(self):

        return (
            f"<MovieProject "
            f"Scenes={self.scene_count()} "
            f"Characters={self.character_count()} "
            f"Backgrounds={self.background_count()}>"
        )