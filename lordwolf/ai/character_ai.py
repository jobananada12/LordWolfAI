"""
LordWolf AI Studio
Character AI
"""

from lordwolf.data.character import Character


class CharacterAI:
    """
    AI керування персонажами.
    """

    def __init__(self):

        self.characters = {}

    def create_character(self, name: str):

        lower = name.lower()

        if lower == "лорд вовк":

            character = Character(
                name="Лорд Вовк",
                species="Wolf",
                gender="Male",
                age="Adult",
                description="Багатий аристократ.",
                clothes="Чорний фрак, бордовий жилет, циліндр.",
                voice="Deep",
                personality="Розумний, спокійний"
            )

        elif lower == "блондинка":

            character = Character(
                name="Блондинка",
                species="Human",
                gender="Female",
                age="Young",
                description="Добра молода дівчина.",
                clothes="Червона сукня.",
                voice="Soft",
                personality="Добра, смілива"
            )

        elif lower == "брюнетка":

            character = Character(
                name="Брюнетка",
                species="Human",
                gender="Female",
                age="Young",
                description="Елегантна жінка.",
                clothes="Біла сукня.",
                voice="Calm",
                personality="Спокійна, розумна"
            )

        elif lower == "король":

            character = Character(
                name="Король",
                species="Human",
                gender="Male",
                age="Old",
                description="Правитель королівства."
            )

        elif lower == "королева":

            character = Character(
                name="Королева",
                species="Human",
                gender="Female",
                age="Adult",
                description="Королева держави."
            )

        elif lower == "лицар":

            character = Character(
                name="Лицар",
                species="Human",
                gender="Male",
                age="Adult",
                description="Хоробрий лицар."
            )

        elif lower == "чаклун":

            character = Character(
                name="Чаклун",
                species="Human",
                gender="Male",
                age="Old",
                description="Могутній чаклун."
            )

        elif lower == "дракон":

            character = Character(
                name="Дракон",
                species="Dragon",
                gender="Unknown",
                age="Ancient",
                description="Величезний дракон."
            )

        else:

            character = Character(
                name=name
            )

        self.characters[character.name] = character

        return character

    def get_character(self, name):

        return self.characters.get(name)

    def get_all(self):

        return list(self.characters.values())

    def remove(self, name):

        self.characters.pop(name, None)

    def clear(self):

        self.characters.clear()