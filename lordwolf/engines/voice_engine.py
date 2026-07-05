"""
LordWolf AI Studio
Voice Engine
"""

from pathlib import Path
from gtts import gTTS
import time


class VoiceEngine:
    """
    Рушій озвучення персонажів.
    Використовує gTTS для генерації голосу.
    """

    def __init__(self, output_dir="audio_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.audio_files = []

    def generate_voice(self, text: str, voice_name: str = "Narrator") -> str:
        """
        Генерує аудіофайл з тексту.
        """
        clean_text = text.strip()
        if not clean_text:
            return ""

        timestamp = int(time.time() * 1000)
        filename = f"voice_{timestamp}.mp3"
        filepath = self.output_dir / filename

        try:
            tts = gTTS(text=clean_text, lang="uk", slow=False)
            tts.save(str(filepath))
            self.audio_files.append(str(filepath))
            return str(filepath)
        except Exception as e:
            print(f"[ERROR] Не вдалося згенерувати голос: {e}")
            return ""

    def generate_character_voice(self, text: str, character_name: str) -> str:
        """
        Генерує голос для конкретного персонажа.
        """
        return self.generate_voice(text, character_name)

    def clear_cache(self):
        """
        Видаляє всі згенеровані аудіофайли.
        """
        for filepath in self.audio_files:
            try:
                Path(filepath).unlink()
            except:
                pass
        self.audio_files.clear()