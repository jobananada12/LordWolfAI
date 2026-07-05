"""
LordWolf AI Studio
Script AI
"""

from typing import Dict, Optional

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

            self.detect_characters(text, current_scene)

            self.detect_backgrounds(text, current_scene)

        if current_scene is not None:

            self.scenes.append(current_scene)

        # Визначаємо головних персонажів для кожної сцени
        for scene in self.scenes:
            self.detect_main_character(scene)

        return self.get_result()

    def detect_characters(self, text: str, scene: Scene):

        names = [

            "лорд вовк",

            "блондинка",

            "брюнетка",

            "королева",

            "король",

            "лицар",

            "чаклун",

            "дракон",

            "вовк"

        ]

        lower = text.lower()

        consumed = lower

        for name in names:

            if name in consumed:

                display_name = name.title()

                self.characters.add(display_name)

                scene.add_character(display_name)

                # Вирізаємо знайдену назву,
                # щоб коротші не знайшлися всередині неї
                consumed = consumed.replace(name, " " * len(name), 1)

    def detect_backgrounds(self, text: str, scene: Scene):

        places = [

            "кімната",

            "кабінет",

            "будинок",

            "печера",

            "дорога",

            "палац",

            "замок",

            "поле",

            "вежа",

            "ліс"

        ]

        lower = text.lower()

        consumed = lower

        for place in places:

            if place in consumed:

                display_name = place.title()

                self.backgrounds.add(display_name)

                scene.add_background(display_name)

                consumed = consumed.replace(place, " " * len(place), 1)

    def detect_main_character(self, scene: Scene):
        """
        Визначає головного персонажа сцени.

        Алгоритм:
        1. Беремо перше речення (перший action)
        2. Шукаємо в ньому персонажів зі списку scene.characters
        3. Якщо знайшли - це головний персонаж сцени
        4. Якщо ні - беремо першого персонажа зі списку
        """

        if not scene.actions:
            return

        # Беремо перше речення сцени
        first_action = scene.actions[0]

        # Шукаємо персонажів у першому реченні
        for character in scene.characters:
            if character.lower() in first_action.lower():
                scene.main_character = character
                return

        # Якщо нікого не знайшли - беремо першого персонажа
        if scene.characters:
            scene.main_character = scene.characters[0]

    def get_result(self):

        return {

            "scene_count": len(self.scenes),

            "characters": sorted(self.characters),

            "backgrounds": sorted(self.backgrounds),

            "scenes": self.scenes

        }