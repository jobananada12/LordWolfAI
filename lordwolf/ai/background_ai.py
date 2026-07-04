"""
LordWolf AI Studio
Background AI
"""

from lordwolf.data.background import Background


class BackgroundAI:
    """
    AI керування фонами.
    """

    def __init__(self):

        self.backgrounds = {}

    def create_background(self, name: str):

        lower = name.lower()

        if lower == "замок":

            background = Background(
                name="Замок",
                category="Castle",
                description="Великий старовинний замок."
            )

        elif lower == "ліс":

            background = Background(
                name="Ліс",
                category="Forest",
                description="Густий зелений ліс."
            )

        elif lower == "печера":

            background = Background(
                name="Печера",
                category="Cave",
                description="Темна кам'яна печера."
            )

        elif lower == "дорога":

            background = Background(
                name="Дорога",
                category="Road",
                description="Стара сільська дорога."
            )

        elif lower == "поле":

            background = Background(
                name="Поле",
                category="Field",
                description="Велике відкрите поле."
            )

        elif lower == "будинок":

            background = Background(
                name="Будинок",
                category="House",
                description="Затишний будинок."
            )

        elif lower == "кімната":

            background = Background(
                name="Кімната",
                category="Room",
                description="Кімната в будинку."
            )

        elif lower == "кабінет":

            background = Background(
                name="Кабінет",
                category="Office",
                description="Робочий кабінет."
            )

        elif lower == "палац":

            background = Background(
                name="Палац",
                category="Palace",
                description="Розкішний палац."
            )

        elif lower == "вежа":

            background = Background(
                name="Вежа",
                category="Tower",
                description="Висока кам'яна вежа."
            )

        else:

            background = Background(
                name=name
            )

        self.backgrounds[background.name] = background

        return background

    def get_background(self, name):

        return self.backgrounds.get(name)

    def get_all(self):

        return list(self.backgrounds.values())

    def remove(self, name):

        self.backgrounds.pop(name, None)

    def clear(self):

        self.backgrounds.clear()