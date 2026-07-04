"""
LordWolf AI Studio
Animation AI
"""

from dataclasses import dataclass


@dataclass
class Animation:

    name: str

    duration: float = 1.0

    loop: bool = False

    description: str = ""


class AnimationAI:
    """
    AI керування анімаціями.
    """

    def __init__(self):

        self.animations = {}

        self.load_default_animations()

    def load_default_animations(self):

        defaults = [

            Animation(
                "idle",
                2.0,
                True,
                "Стоїть спокійно"
            ),

            Animation(
                "walk",
                1.2,
                True,
                "Ходьба"
            ),

            Animation(
                "run",
                0.8,
                True,
                "Біг"
            ),

            Animation(
                "jump",
                0.7,
                False,
                "Стрибок"
            ),

            Animation(
                "attack",
                0.9,
                False,
                "Атака"
            ),

            Animation(
                "talk",
                1.0,
                True,
                "Розмова"
            ),

            Animation(
                "happy",
                1.0,
                False,
                "Радість"
            ),

            Animation(
                "sad",
                1.0,
                False,
                "Сум"
            )

        ]

        for animation in defaults:

            self.animations[animation.name] = animation

    def get_animation(self, name):

        return self.animations.get(name)

    def get_all(self):

        return list(self.animations.values())

    def add_animation(self, animation):

        self.animations[animation.name] = animation

    def remove_animation(self, name):

        if name in self.animations:

            del self.animations[name]

    def clear(self):

        self.animations.clear()

        self.load_default_animations()