"""
LordWolf AI Studio
Scene Manager
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Scene:

    id: int

    title: str

    background: str = ""

    characters: List[str] = field(default_factory=list)

    actions: List[str] = field(default_factory=list)

    duration: float = 5.0


class SceneManager:

    def __init__(self):

        self.scenes = []

    def create_scene(self, title):

        scene = Scene(

            id=len(self.scenes) + 1,

            title=title

        )

        self.scenes.append(scene)

        return scene

    def add_scene(self, scene):

        self.scenes.append(scene)

    def remove_scene(self, scene_id):

        self.scenes = [

            scene

            for scene in self.scenes

            if scene.id != scene_id

        ]

    def get_scene(self, scene_id):

        for scene in self.scenes:

            if scene.id == scene_id:

                return scene

        return None

    def get_all(self):

        return self.scenes

    def clear(self):

        self.scenes.clear()