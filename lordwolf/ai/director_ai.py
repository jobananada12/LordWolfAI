"""
LordWolf AI Studio
Director AI - БЕЗ ФІКСОВАНОЇ ТРИВАЛОСТІ
"""

from pathlib import Path
from lordwolf.ai.script_ai import ScriptAI
from lordwolf.ai.character_ai import CharacterAI
from lordwolf.ai.background_ai import BackgroundAI
from lordwolf.ai.animation_ai import AnimationAI
from lordwolf.ai.voice_ai import VoiceAI

from lordwolf.data.project import MovieProject

from lordwolf.engines.voice_engine import VoiceEngine
from lordwolf.engines.image_engine import ImageEngine
from lordwolf.engines.video_engine import VideoEngine


class DirectorAI:
    """
    Головний координатор AI.
    """

    def __init__(self):
        self.script_ai = ScriptAI()
        self.character_ai = CharacterAI()
        self.background_ai = BackgroundAI()
        self.animation_ai = AnimationAI()
        self.voice_ai = VoiceAI()

        self.voice_engine = VoiceEngine()
        self.image_engine = ImageEngine()
        self.video_engine = VideoEngine()

        self.project = MovieProject()
        self.dialog_list = []

    def create_movie(self, script):
        print("[INFO] DirectorAI: Початок")

        self.dialog_list = []
        self.video_engine.clear()
        self.project.clear()
        self.project.script = script

        result = self.script_ai.analyze(script)
        self.project.scenes = result["scenes"]
        print(f"[INFO] ScriptAI: {result['scene_count']} сцен")

        for name in result["characters"]:
            char = self.character_ai.create_character(name)
            char.image_path = self.image_engine.generate_character(name)
            self.project.characters.append(char)

        for name in result["backgrounds"]:
            bg = self.background_ai.create_background(name)
            bg.image_path = self.image_engine.generate_background(name)
            self.project.backgrounds.append(bg)

        self.project.animations = self.animation_ai.get_all()
        self.project.voices = self.voice_ai.get_all()

        self._collect_dialogs()
        self._generate_audio()
        self._create_video()

        print("[INFO] DirectorAI: Готово!")
        return self.project

    def _collect_dialogs(self):
        for scene in self.project.scenes:
            for action in scene.actions:
                if ":" not in action:
                    continue

                speaker = None
                text = action

                for char in scene.characters:
                    if char + ":" in text:
                        speaker = char
                        text = text.replace(char + ":", "").strip()
                        break

                if not speaker:
                    speaker = scene.main_character or "Narrator"

                if text:
                    self.dialog_list.append({
                        "speaker": speaker,
                        "text": text,
                        "audio_path": None
                    })
                    print(f"[DIALOG] {speaker}: {text[:40]}...")

    def _generate_audio(self):
        for i, dialog in enumerate(self.dialog_list):
            audio_path = self.voice_engine.generate_character_voice(
                dialog["text"], dialog["speaker"]
            )
            dialog["audio_path"] = audio_path
            print(f"[AUDIO] {i+1:02d}: {dialog['speaker']} -> {Path(audio_path).name if audio_path else 'None'}")

    def _create_video(self):
        print(f"[INFO] Створення {len(self.dialog_list)} сцен")

        for dialog in self.dialog_list:
            speaker = dialog["speaker"]
            audio_path = dialog["audio_path"]

            char_path = None
            for char in self.project.characters:
                if char.name == speaker:
                    char_path = char.image_path
                    break

            if not char_path:
                char_path = str(self.image_engine.characters_path / "default.png")

            # 🔥 НЕ ПЕРЕДАЄМО duration, щоб він визначився з аудіо
            self.video_engine.create_scene(
                image_path=char_path,
                audio_path=audio_path
            )

        self.video_engine.add_end_pause(2.0)
        print("[INFO] Фінальна пауза: 2.0с")

    def render_movie(self, filename="movie.mp4"):
        return self.video_engine.render_movie(filename)

    def reset(self):
        self.project.clear()
        self.character_ai.clear()
        self.background_ai.clear()
        self.video_engine.clear()
        self.dialog_list = []