"""
LordWolf AI Studio
Image Engine
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import unicodedata
import re


class ImageEngine:
    """
    Рушій генерації зображень.
    """

    def __init__(self, assets_path="assets"):

        self.assets_path = Path(assets_path)

        self.characters_path = self.assets_path / "characters"
        self.backgrounds_path = self.assets_path / "backgrounds"
        self.props_path = self.assets_path / "props"

        self.characters_path.mkdir(parents=True, exist_ok=True)
        self.backgrounds_path.mkdir(parents=True, exist_ok=True)
        self.props_path.mkdir(parents=True, exist_ok=True)

        print(f"[INFO] ImageEngine ініціалізовано")
        print(f"  - Characters: {self.characters_path}")
        print(f"  - Backgrounds: {self.backgrounds_path}")
        print(f"  - Props: {self.props_path}")

    def _slugify(self, name: str) -> str:
        """
        Перетворює кирилицю в латиницю для безпечних імен файлів.
        """
        # Транслітерація української → латиниця
        translit_map = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g',
            'д': 'd', 'е': 'e', 'є': 'ye', 'ж': 'zh', 'з': 'z',
            'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k',
            'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
            'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
            'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
            'ь': '', 'ю': 'yu', 'я': 'ya',
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G',
            'Д': 'D', 'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z',
            'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K',
            'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P',
            'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F',
            'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
            'Ь': '', 'Ю': 'Yu', 'Я': 'Ya'
        }

        result = ''
        for char in name:
            if char in translit_map:
                result += translit_map[char]
            elif char.isalnum() or char == ' ':
                result += char
            else:
                result += ''

        # Замінюємо пробіли на нижнє підкреслення
        result = result.replace(' ', '_')
        # Видаляємо зайві символи
        result = re.sub(r'[^a-zA-Z0-9_]', '', result)

        return result

    def generate_character(self, name: str, prompt: str = None) -> str:
        """
        Генерує зображення персонажа.
        """

        # Створюємо безпечне ім'я файлу
        safe_name = self._slugify(name)
        file_path = self.characters_path / f"{safe_name}.png"

        # Зберігаємо оригінальне ім'я для тексту на зображенні
        display_name = name

        print(f"[INFO] Генерація персонажа: {name} -> {file_path}")

        # Створюємо кольоровий квадрат з іменем
        img = Image.new("RGB", (256, 256), color=self._get_color(name))
        draw = ImageDraw.Draw(img)

        # Додаємо текст
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()

        draw.text((10, 120), display_name, fill="white", font=font)

        img.save(file_path)
        print(f"[INFO] Збережено: {file_path}")

        return str(file_path)

    def generate_background(self, name: str, prompt: str = None) -> str:
        """
        Генерує зображення фону.
        """

        safe_name = self._slugify(name)
        file_path = self.backgrounds_path / f"{safe_name}.png"
        display_name = name

        print(f"[INFO] Генерація фону: {name} -> {file_path}")

        img = Image.new("RGB", (512, 384), color=(50, 50, 80))
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()

        draw.text((10, 180), display_name, fill="white", font=font)

        img.save(file_path)
        print(f"[INFO] Збережено: {file_path}")

        return str(file_path)

    def generate_prop(self, name: str, prompt: str = None) -> str:
        """
        Генерує зображення пропа.
        """

        safe_name = self._slugify(name)
        file_path = self.props_path / f"{safe_name}.png"

        img = Image.new("RGB", (128, 128), color=(100, 100, 100))
        img.save(file_path)

        return str(file_path)

    def _get_color(self, name: str) -> tuple:
        """
        Повертає колір на основі імені.
        """

        colors = {
            "Лорд Вовк": (80, 40, 120),
            "Вовк": (80, 40, 120),
            "Блондинка": (255, 200, 100),
            "Брюнетка": (150, 80, 40),
            "Король": (200, 50, 50),
            "Королева": (200, 50, 150),
            "Лицар": (150, 150, 200),
            "Чаклун": (50, 50, 150),
            "Дракон": (200, 50, 0),
        }

        return colors.get(name, (100, 100, 100))

    def get_character_path(self, name: str) -> str:
        safe_name = self._slugify(name)
        return str(self.characters_path / f"{safe_name}.png")

    def get_background_path(self, name: str) -> str:
        safe_name = self._slugify(name)
        return str(self.backgrounds_path / f"{safe_name}.png")