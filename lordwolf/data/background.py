"""
LordWolf AI Studio
Data Model: Background
"""

from dataclasses import dataclass


@dataclass
class Background:
    """
    Єдина модель фону для всієї системи.
    """

    name: str
    category: str = "Unknown"

    description: str = ""

    weather: str = "Clear"
    daytime: str = "Day"

    # майбутні AI генерації
    image_path: str = ""
    style: str = ""