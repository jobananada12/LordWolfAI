"""
LordWolf AI Studio
Image Engine
"""

from pathlib import Path


class ImageEngine:
    """
    Рушій генерації зображень.
    У майбутньому тут будуть:
    - Stable Diffusion
    - ComfyUI
    - Flux
    - локальні моделі
    """

    def __init__(self, assets_path="assets"):

        self.assets_path = Path(assets_path)

        self.characters_path = self.assets_path / "characters"
        self.backgrounds_path = self.assets_path / "backgrounds"
        self.props_path = self.assets_path / "props"

        self.characters_path.mkdir(parents=True, exist_ok=True)
        self.backgrounds_path.mkdir(parents=True, exist_ok=True)
        self.props_path.mkdir(parents=True, exist_ok=True)

    def generate_character(self, name: str, prompt: str = None):

        """
        Поки що заглушка.
        Пізніше тут буде AI генерація PNG.
        """

        file_path = self.characters_path / f"{name}.png"

        # TODO: підключити AI генерацію
        # зараз просто створюємо пустий файл як тест

        file_path.touch()

        return str(file_path)

    def generate_background(self, name: str, prompt: str = None):

        file_path = self.backgrounds_path / f"{name}.png"

        file_path.touch()

        return str(file_path)

    def generate_prop(self, name: str, prompt: str = None):

        file_path = self.props_path / f"{name}.png"

        file_path.touch()

        return str(file_path)

    def get_character_path(self, name: str):

        return str(self.characters_path / f"{name}.png")

    def get_background_path(self, name: str):

        return str(self.backgrounds_path / f"{name}.png")