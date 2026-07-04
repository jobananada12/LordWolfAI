"""
LordWolf AI Studio
Character Manager
"""

from typing import Dict


class CharacterManager:
    """
    Керує всіма персонажами проєкту.
    """

    def __init__(self):

        self.characters: Dict[str, object] = {}

    def add_character(self, character):

        self.characters[character.name] = character

    def remove_character(self, name):

        if name in self.characters:
            del self.characters[name]

    def get_character(self, name):

        return self.characters.get(name)

    def exists(self, name):

        return name in self.characters

    def get_all(self):

        return list(self.characters.values())

    def count(self):

        return len(self.characters)

    def clear(self):

        self.characters.clear()