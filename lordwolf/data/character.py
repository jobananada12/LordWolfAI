"""
LordWolf AI Studio
Data Model: Character
"""

from dataclasses import dataclass


@dataclass
class Character:
    """
    Єдина модель персонажа для всієї системи.
    Використовується AI, Engine і UI.
    """

    name: str
    species: str = "Unknown"
    gender: str = "Unknown"
    age: str = "Unknown"

    description: str = ""
    clothes: str = ""
    voice: str = ""
    personality: str = ""

    # майбутні поля для анімації
    model_path: str = ""
    texture_path: str = ""
    animation_set: str = ""