"""
LordWolf AI Studio
Voice Engine - РОЗШИРЕНИЙ ДІАПАЗОН
"""

from pathlib import Path
import asyncio
import edge_tts
import time


class VoiceEngine:
    def __init__(self, output_dir="audio_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.audio_files = []

        # 🔥 РОЗШИРЕНІ НАЛАШТУВАННЯ ДЛЯ КОЖНОГО ПЕРСОНАЖА
        self.voice_presets = {
            # ===== ЧОЛОВІЧІ ПЕРСОНАЖІ (uk-UA-OstapNeural) =====
            "Лорд Вовк": {
                "voice": "uk-UA-OstapNeural",
                "rate": "-10%",      # повільний, солідний
                "pitch": "-4Hz",     # нижчий, грубуватий
            },
            "Вовк": {
                "voice": "uk-UA-OstapNeural",
                "rate": "-10%",
                "pitch": "-4Hz",
            },
            "Дракон": {
                "voice": "uk-UA-OstapNeural",
                "rate": "-30%",      # дуже повільний, грізний
                "pitch": "-12Hz",    # дуже низький
            },
            "Чаклун": {
                "voice": "uk-UA-OstapNeural",
                "rate": "-20%",      # повільний, таємничий
                "pitch": "-8Hz",     # низький, моторошний
            },
            "Король": {
                "voice": "uk-UA-OstapNeural",
                "rate": "-8%",       # величний, повільний
                "pitch": "-2Hz",     # трохи нижче
            },
            "Лицар": {
                "voice": "uk-UA-OstapNeural",
                "rate": "0%",        # нормальний
                "pitch": "0Hz",      # нормальний
            },
            "Монстр": {
                "voice": "uk-UA-OstapNeural",
                "rate": "-35%",      # дуже повільний
                "pitch": "-14Hz",    # дуже низький
            },

            # ===== ЖІНОЧІ ПЕРСОНАЖІ (uk-UA-PolinaNeural) =====
            "Блондинка": {
                "voice": "uk-UA-PolinaNeural",
                "rate": "+25%",      # швидка, дзвінка
                "pitch": "+10Hz",    # дуже висока
            },
            "Брюнетка": {
                "voice": "uk-UA-PolinaNeural",
                "rate": "+10%",      # середня швидкість
                "pitch": "+4Hz",     # вища за норму
            },
            "Королева": {
                "voice": "uk-UA-PolinaNeural",
                "rate": "-8%",       # повільна, велична
                "pitch": "+2Hz",     # трохи вища
            },
            "Дівчинка": {
                "voice": "uk-UA-PolinaNeural",
                "rate": "+35%",      # дуже швидка
                "pitch": "+14Hz",    # дуже висока
            },
            "Відьма": {
                "voice": "uk-UA-PolinaNeural",
                "rate": "-15%",      # повільна
                "pitch": "-4Hz",     # низька для жінки
            },

            # ===== ОПОВІДАЧ =====
            "Оповідач": {
                "voice": "uk-UA-OstapNeural",
                "rate": "-5%",
                "pitch": "0Hz",
            },

            # ===== ЗА ЗАМОВЧУВАННЯМ =====
            "default": {
                "voice": "uk-UA-PolinaNeural",
                "rate": "0%",
                "pitch": "0Hz",
            }
        }

    def generate_character_voice(self, text: str, character_name: str) -> str:
        clean_text = text.strip()
        if not clean_text:
            return None

        preset = self.voice_presets.get(character_name, self.voice_presets["default"])
        voice = preset["voice"]
        rate = preset.get("rate", "0%")
        pitch = preset.get("pitch", "0Hz")

        timestamp = int(time.time() * 1000)
        filename = f"voice_{timestamp}.mp3"
        filepath = self.output_dir / filename

        try:
            communicate = edge_tts.Communicate(
                text=clean_text,
                voice=voice,
                rate=rate,
                pitch=pitch
            )

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(communicate.save(str(filepath)))
            loop.close()

            self.audio_files.append(str(filepath))
            print(f"[VOICE] {character_name} | {voice} | rate={rate}, pitch={pitch} -> {filename}")
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