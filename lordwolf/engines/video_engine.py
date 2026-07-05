"""
LordWolf AI Studio
Video Engine - АВТОМАТИЧНА ТРИВАЛІСТЬ З АУДІО
"""

from pathlib import Path
import cv2
import subprocess
import tempfile
from mutagen.mp3 import MP3
import numpy as np


class VideoEngine:
    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.scenes = []
        self.end_pause = 0.0

    def create_scene(self, image_path, audio_path=None, duration=None):
        self.scenes.append({
            "image": image_path,
            "audio": audio_path,
            "duration": duration  # якщо None, визначиться автоматично
        })
        print(f"[DEBUG] Додано сцену: {Path(image_path).name} | аудіо: {Path(audio_path).name if audio_path else 'None'}")

    def add_end_pause(self, duration):
        self.end_pause = duration
        print(f"[DEBUG] Встановлено фінальну паузу: {duration}с")

    def render_movie(self, filename="lordwolf_movie.mp4", fps=24):
        if not self.scenes:
            print("[ERROR] Немає сцен")
            return None

        print(f"[INFO] Рендеринг: {len(self.scenes)} сцен")

        first_img = self.scenes[0]["image"]
        if not Path(first_img).exists():
            print(f"[ERROR] Немає зображення: {first_img}")
            return None

        img = cv2.imread(str(first_img))
        if img is None:
            print(f"[ERROR] Не вдалося завантажити: {first_img}")
            return None

        h, w = img.shape[:2]
        print(f"[INFO] Розмір: {w}x{h}")

        black_frame = np.zeros((h, w, 3), dtype=np.uint8)
        output_path = self.output_dir / filename

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            audio_files = []
            total_frames = 0
            total_duration = 0.0

            for i, scene in enumerate(self.scenes):
                print(f"[INFO] Сцена {i+1}/{len(self.scenes)}")

                img_path = scene["image"]
                if not Path(img_path).exists():
                    print(f"[WARNING] Зображення не знайдено: {img_path}")
                    continue

                img = cv2.imread(str(img_path))
                if img is None:
                    print(f"[WARNING] Не вдалося завантажити: {img_path}")
                    continue

                if img.shape[1] != w or img.shape[0] != h:
                    img = cv2.resize(img, (w, h))

                audio_path = scene.get("audio")
                duration = scene.get("duration")

                # 🔥 Якщо duration не задано - беремо з аудіо
                if duration is None:
                    if audio_path and Path(audio_path).exists():
                        try:
                            audio = MP3(audio_path)
                            duration = audio.info.length
                            print(f"[INFO]   Аудіо: {Path(audio_path).name} ({duration:.2f}с)")
                            audio_files.append(audio_path)
                        except Exception as e:
                            print(f"[WARNING] Не вдалося прочитати аудіо: {e}")
                            duration = 3.0
                    else:
                        duration = 3.0
                        print(f"[INFO]   Аудіо: відсутнє, duration={duration:.2f}с")
                else:
                    # Якщо duration задано, але аудіо довше - використовуємо більше
                    if audio_path and Path(audio_path).exists():
                        try:
                            audio = MP3(audio_path)
                            if audio.info.length > duration:
                                duration = audio.info.length
                            audio_files.append(audio_path)
                            print(f"[INFO]   Аудіо: {Path(audio_path).name} ({audio.info.length:.2f}с)")
                        except:
                            pass

                # Якщо все ще duration не визначено
                if duration is None or duration == 0:
                    duration = 3.0

                num_frames = int(duration * fps)
                print(f"[INFO]   Тривалість: {duration:.2f}с, кадрів: {num_frames}")
                total_duration += duration

                for _ in range(num_frames):
                    frame_path = tmp_path / f"frame_{total_frames:06d}.png"
                    cv2.imwrite(str(frame_path), img)
                    total_frames += 1

            # Фінальна пауза
            if self.end_pause > 0:
                end_frames = int(self.end_pause * fps)
                print(f"[INFO] Фінальна пауза: {self.end_pause:.2f}с ({end_frames} кадрів)")
                for _ in range(end_frames):
                    frame_path = tmp_path / f"frame_{total_frames:06d}.png"
                    cv2.imwrite(str(frame_path), black_frame)
                    total_frames += 1
                total_duration += self.end_pause

            if total_frames == 0:
                print("[ERROR] Немає кадрів")
                return None

            print(f"[INFO] Всього кадрів: {total_frames}")
            print(f"[INFO] Загальна тривалість: {total_duration:.2f}с")

            video_only = tmp_path / "video_only.mp4"
            cmd = [
                "ffmpeg", "-y",
                "-framerate", str(fps),
                "-i", str(tmp_path / "frame_%06d.png"),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                str(video_only)
            ]
            subprocess.run(cmd, capture_output=True, check=True)

            if audio_files:
                print(f"[INFO] Додавання звуку ({len(audio_files)} файлів)")

                list_file = tmp_path / "audio_list.txt"
                with open(list_file, "w") as f:
                    for af in audio_files:
                        f.write(f"file '{Path(af).absolute()}'\n")

                combined = tmp_path / "combined.mp3"
                cmd = [
                    "ffmpeg", "-y",
                    "-f", "concat",
                    "-safe", "0",
                    "-i", str(list_file),
                    "-c", "copy",
                    str(combined)
                ]
                subprocess.run(cmd, capture_output=True, check=True)

                if combined.exists():
                    cmd = [
                        "ffmpeg", "-y",
                        "-i", str(video_only),
                        "-i", str(combined),
                        "-c:v", "copy",
                        "-c:a", "aac",
                        "-shortest",
                        str(output_path)
                    ]
                    subprocess.run(cmd, capture_output=True, check=True)
                    print("[INFO] Звук додано")
                else:
                    import shutil
                    shutil.copy(video_only, output_path)
            else:
                import shutil
                shutil.copy(video_only, output_path)

        if output_path.exists():
            size = output_path.stat().st_size / 1024 / 1024
            print(f"[SUCCESS] Відео: {output_path} ({size:.2f} MB)")
            return str(output_path)

        print("[ERROR] Відео не створено")
        return None

    def clear(self):
        self.scenes.clear()
        self.end_pause = 0.0
        print("[DEBUG] Очищено сцени")