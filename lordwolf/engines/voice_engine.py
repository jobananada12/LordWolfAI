"""
LordWolf AI Studio
Voice Engine - ВИПРАВЛЕНА ВЕРСІЯ (правильний пошук голосів)
"""

from pathlib import Path
import time
from elevenlabs.client import ElevenLabs


class VoiceEngine:
    def __init__(self, output_dir="audio_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.audio_files = []

        self.api_key = "sk_7ed7f2945b9079908cd4df02064e1f09a28301e2b329db0f"
        self.client = ElevenLabs(api_key=self.api_key)

        try:
            response = self.client.voices.search()
            self.voices = response.voices

            # 🔥 СТВОРЮЄМО СЛОВНИК ПРОСТИХ ІМЕН → VOICE_ID
            self.voice_dict = {}
            for v in self.voices:
                # Витягуємо просте ім'я (до " - ")
                if " - " in v.name:
                    simple_name = v.name.split(" - ")[0].strip()
                else:
                    simple_name = v.name.strip()
                self.voice_dict[simple_name] = v.voice_id

            print("[INFO] ElevenLabs: підключено!")
            print(f"[INFO] Доступно голосів: {len(self.voices)}")
            for v in self.voices[:10]:
                simple_name = v.name.split(" - ")[0].strip() if " - " in v.name else v.name.strip()
                print(f"  - {simple_name} (ID: {v.voice_id[:8]}...)")
        except Exception as e:
            print(f"[ERROR] Не вдалося отримати голоси: {e}")
            self.voices = []
            self.voice_dict = {}

        default_voice_id = self.voices[0].voice_id if self.voices else None

        # 🔥 РОЗПОДІЛ ЗА СТАТТЮ (прості імена)
        self.male_voices = ["Roger", "Charlie", "George", "Harry", "Callum", "River", "Liam"]
        self.female_voices = ["Sarah", "Laura", "Alice", "Dorothy", "Grace", "Bella"]

        # 🔥 ПЕРСОНАЛЬНІ ПРИЗНАЧЕННЯ (тепер працюватимуть!)
        self.custom_voice_map = {
            "Лорд Вовк": self._find_voice(["Roger", "Charlie", "George"]),
            "Вовк": self._find_voice(["Roger", "Charlie", "George"]),
            "Дракон": self._find_voice(["Harry", "Charlie", "Roger"]),
            "Чаклун": self._find_voice(["George", "Callum", "Roger"]),
            "Король": self._find_voice(["Charlie", "Roger", "George"]),
            "Лицар": self._find_voice(["Charlie", "Harry", "Roger"]),
            "Монстр": self._find_voice(["Harry", "Charlie", "Roger"]),
            "Оповідач": self._find_voice(["George", "Roger", "Charlie"]),
            "Блондинка": self._find_voice(["Sarah", "Laura", "Alice"]),
            "Брюнетка": self._find_voice(["Alice", "Laura", "Sarah"]),
            "Королева": self._find_voice(["Laura", "Alice", "Sarah"]),
            "Дівчинка": self._find_voice(["Sarah", "Laura", "Alice"]),
            "Відьма": self._find_voice(["Laura", "Alice", "Sarah"]),
        }

        self.default_voice_id = default_voice_id

    def _find_voice(self, preferred_names):
        for name in preferred_names:
            if name in self.voice_dict:
                return self.voice_dict[name]
        # Якщо жоден не знайдено, шукаємо за статтю
        for name in self.male_voices + self.female_voices:
            if name in self.voice_dict:
                return self.voice_dict[name]
        if self.voices:
            return self.voices[0].voice_id
        return None

    def _get_gender_for_character(self, character_name):
        male_keywords = ["Лорд", "Вовк", "Дракон", "Чаклун", "Король", "Лицар", "Монстр", "Оповідач"]
        female_keywords = ["Блондинка", "Брюнетка", "Королева", "Дівчинка", "Відьма"]
        for word in male_keywords:
            if word in character_name:
                return "male"
        for word in female_keywords:
            if word in character_name:
                return "female"
        return "unknown"

    def _get_voice_for_character(self, character_name):
        # 1. Спочатку перевіряємо кастомне призначення
        if character_name in self.custom_voice_map:
            voice_id = self.custom_voice_map[character_name]
            if voice_id:
                return voice_id

        # 2. Якщо немає, визначаємо за статтю
        gender = self._get_gender_for_character(character_name)
        if gender == "male":
            for name in self.male_voices:
                if name in self.voice_dict:
                    return self.voice_dict[name]
        elif gender == "female":
            for name in self.female_voices:
                if name in self.voice_dict:
                    return self.voice_dict[name]

        # 3. Якщо нічого не підійшло, беремо дефолтний
        return self.default_voice_id

    def generate_character_voice(self, text: str, character_name: str) -> str:
        clean_text = text.strip()
        if not clean_text:
            return None

        voice_id = self._get_voice_for_character(character_name)
        if not voice_id:
            print(f"[ERROR] Немає голосу для {character_name}")
            return None

        timestamp = int(time.time() * 1000)
        filename = f"voice_{timestamp}.mp3"
        filepath = self.output_dir / filename

        try:
            audio_generator = self.client.text_to_speech.convert(
                voice_id=voice_id,
                text=clean_text,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
                language_code="uk",
            )
            audio_bytes = b''.join(audio_generator)
            with open(filepath, "wb") as f:
                f.write(audio_bytes)
            self.audio_files.append(str(filepath))

            # Шукаємо просте ім'я для логу
            voice_name = "невідомий"
            for name, vid in self.voice_dict.items():
                if vid == voice_id:
                    voice_name = name
                    break
            print(f"[VOICE] {character_name} -> {voice_name} (стать: {self._get_gender_for_character(character_name)})")
            return str(filepath)
        except Exception as e:
            print(f"[ERROR] {character_name}: {e}")
            return None

    def clear_cache(self):
        for filepath in self.audio_files:
            try:
                Path(filepath).unlink()
            except:
                pass
        self.audio_files.clear()