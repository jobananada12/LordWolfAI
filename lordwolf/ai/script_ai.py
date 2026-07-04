"""
LordWolf AI Studio
Script AI
"""

from typing import Dict

from lordwolf.data.scene import Scene


class ScriptAI:
    """
    AI аналізатор сценарію.

    Перетворює текст сценарію
    у список сцен, персонажів і фонів.
    """

    def __init__(self):

        self.reset()

    def reset(self):

        self.characters = set()

        self.backgrounds = set()

        self.scenes = []

    def analyze(self, script: str) -> Dict:

        self.reset()

        current_scene = None

        scene_number = 1

        for line in script.splitlines():

            text = line.strip()

            if not text:
                continue

            if text.lower().startswith("сцена"):

                if current_scene is not None:
                    self.scenes.append(current_scene)

                current_scene = Scene(
                    number=scene_number,
                    title=text
                )

                scene_number += 1

                continue

            if current_scene is None:

                current_scene = Scene(
                    number=scene_number,
                    title="Сцена 1"
                )

            current_scene.add_action(text)

            self.detect_characters(text)

            self.detect_backgrounds(text)

        if current_scene is not None:

            self.scenes.append(current_scene)

        return self.get_result()

    def detect_characters(self, text: str):

        names = [

            "вовк",

            "лорд вовк",

            "блондинка",

            "брюнетка",

            "король",

            "королева",

            "лицар",

            "чаклун",

            "дракон"

        ]

        lower = text.lower()

        for name in names:

            if name in lower:

                self.characters.add(name.title())

    def detect_backgrounds(self, text: str):

        places = [

            "замок",

            "ліс",

            "печера",

            "дорога",

            "поле",

            "будинок",

            "кімната",

            "кабінет",

            "палац",

            "вежа"

        ]

        lower = text.lower()

        for place in places:

            if place in lower:

                self.backgrounds.add(place.title())

    def get_result(self):

        return {

            "scene_count": len(self.scenes),

            "characters": sorted(self.characters),

            "backgrounds": sorted(self.backgrounds),

            "scenes": self.scenes

        }