"""
TEST SIMPLE - Мінімальний тест для перевірки логіки
"""

import os
import re
from pathlib import Path
import cv2
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
import time
from mutagen.mp3 import MP3

# ============================================
# 0. ТРАНСЛІТЕРАЦІЯ ДЛЯ ІМЕН ФАЙЛІВ
# ============================================

def slugify(name: str) -> str:
    """Перетворює кирилицю в латиницю для безпечних імен файлів."""
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
    result = result.replace(' ', '_')
    result = re.sub(r'[^a-zA-Z0-9_]', '', result)
    return result

# ============================================
# 1. СЦЕНАРІЙ (ваш текст)
# ============================================
SCRIPT = """
СЦЕНА 1

Лорд Вовк сидить у замку біля каміна.

У двері стукають.

Лорд Вовк: Хто там?

Заходить Блондинка.

Блондинка: Добрий вечір, пане Лорде!

Лорд Вовк: О, Блондинка! Які вітри тебе занесли?

Блондинка: Мені потрібна твоя допомога!

СЦЕНА 2

Лорд Вовк і Блондинка йдуть через ліс.

Лорд Вовк: Куди ми йдемо?

Блондинка: До печери Дракона!

Раптом вони чують гучний звук.

Дракон: Хто сміє наближатися до моєї печери?

СЦЕНА 3

Лорд Вовк і Блондинка стоять перед печерою.

Лорд Вовк: Ми прийшли з миром!

Дракон: Я вам не вірю!

Блондинка: Ми хочемо попросити тебе про допомогу.

Дракон: Говоріть!

Лорд Вовк: У королівстві з'явився злий чаклун.

Дракон: Я знаю про цього чаклуна!

СЦЕНА 4

Лорд Вовк, Блондинка і Дракон летять над лісом.

Блондинка: Я так боюся висоти!

Лорд Вовк: Не бійся, це чудово!

Дракон: Я відчуваю злого чаклуна!

Лорд Вовк: Он він, біля старого замку!

СЦЕНА 5

Чаклун стоїть біля замку.

Чаклун: Ви не переможете мене!

Дракон: Ми покажемо тобі!

Лорд Вовк: Разом ми сильніші!

Блондинка: Ми переможемо зло!

Всі разом кидаються на чаклуна.

Дракон: Перемога за нами!

Лорд Вовк: Ми врятували королівство!

Кінець.
"""

# ============================================
# 2. ПАРСИНГ СЦЕНАРІЮ
# ============================================

def parse_script(script_text):
    """
    Парсить сценарій і повертає список діалогів.
    Кожен діалог = {"speaker": "ім'я", "text": "текст"}
    """
    dialogs = []
    lines = script_text.strip().splitlines()
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if ":" in line:
            parts = line.split(":", 1)
            speaker = parts[0].strip()
            text = parts[1].strip()
            
            if speaker.upper() != "СЦЕНА" and speaker.lower() != "кінець":
                dialogs.append({
                    "speaker": speaker,
                    "text": text
                })
    
    return dialogs

# ============================================
# 3. ГЕНЕРАЦІЯ ЗОБРАЖЕНЬ ПЕРСОНАЖІВ
# ============================================

def generate_character_image(name, output_dir="test_assets"):
    """
    Створює просте зображення персонажа з іменем.
    Використовує транскрипцію для імені файлу.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Кольори для різних персонажів
    colors = {
        "Лорд Вовк": (80, 40, 120),
        "Блондинка": (255, 200, 100),
        "Дракон": (200, 50, 0),
        "Чаклун": (50, 50, 150),
    }
    
    color = colors.get(name, (100, 100, 100))
    
    img = Image.new("RGB", (256, 256), color=color)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((10, 120), name, fill="white", font=font)
    
    # 🔥 ВИКОРИСТОВУЄМО ТРАНСКРИПЦІЮ ДЛЯ ІМЕНІ ФАЙЛУ
    safe_name = slugify(name)
    file_path = output_path / f"{safe_name}.png"
    img.save(file_path)
    return str(file_path)

# ============================================
# 4. ГЕНЕРАЦІЯ АУДІО
# ============================================

def generate_audio(text, speaker, output_dir="test_audio"):
    """
    Генерує аудіофайл для тексту.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = int(time.time() * 1000)
    filename = f"voice_{timestamp}.mp3"
    filepath = output_path / filename
    
    try:
        tts = gTTS(text=text, lang="uk", slow=False)
        tts.save(str(filepath))
        return str(filepath)
    except Exception as e:
        print(f"[ERROR] {e}")
        return None

# ============================================
# 5. СТВОРЕННЯ ВІДЕО
# ============================================

def create_video(dialogs, output_filename="test_movie.mp4", fps=24):
    """
    Створює відео з діалогів.
    """
    print(f"[INFO] Створення відео з {len(dialogs)} діалогів")
    
    # Генеруємо зображення та аудіо
    audio_files = []
    image_files = []
    scenes = []
    
    for i, dialog in enumerate(dialogs):
        speaker = dialog["speaker"]
        text = dialog["text"]
        
        print(f"[INFO] Діалог {i+1}: {speaker} -> {text[:30]}...")
        
        # Зображення персонажа
        img_path = generate_character_image(speaker)
        image_files.append(img_path)
        
        # Аудіо
        audio_path = generate_audio(text, speaker)
        if audio_path:
            audio_files.append(audio_path)
            try:
                audio = MP3(audio_path)
                duration = audio.info.length
            except:
                duration = 3.0
        else:
            duration = 3.0
        
        scenes.append({
            "image": img_path,
            "audio": audio_path,
            "duration": duration
        })
    
    # Створюємо відео
    first_img = cv2.imread(scenes[0]["image"])
    if first_img is None:
        print("[ERROR] Не вдалося завантажити перше зображення")
        return None
        
    h, w = first_img.shape[:2]
    
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        total_frames = 0
        all_audio = []
        
        for i, scene in enumerate(scenes):
            img = cv2.imread(scene["image"])
            if img is None:
                print(f"[WARNING] Не вдалося завантажити зображення для сцени {i+1}")
                continue
            
            if img.shape[1] != w or img.shape[0] != h:
                img = cv2.resize(img, (w, h))
            
            duration = scene["duration"]
            audio_path = scene["audio"]
            
            if audio_path and Path(audio_path).exists():
                all_audio.append(audio_path)
                try:
                    audio = MP3(audio_path)
                    duration = max(duration, audio.info.length)
                except:
                    pass
            
            num_frames = int(duration * fps)
            for _ in range(num_frames):
                frame_path = tmp_path / f"frame_{total_frames:06d}.png"
                cv2.imwrite(str(frame_path), img)
                total_frames += 1
        
        if total_frames == 0:
            print("[ERROR] Немає кадрів")
            return None
        
        print(f"[INFO] Всього кадрів: {total_frames}")
        
        # Створюємо відео без звуку
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
        
        # Додаємо звук
        output_path = Path(output_filename)
        if all_audio:
            print(f"[INFO] Додавання звуку ({len(all_audio)} файлів)")
            
            list_file = tmp_path / "audio_list.txt"
            with open(list_file, "w") as f:
                for af in all_audio:
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
    
    return None

# ============================================
# 6. ГОЛОВНА ФУНКЦІЯ
# ============================================

def main():
    print("=" * 60)
    print("ТЕСТОВИЙ ПРОЕКТ: Парсинг сценарію + відео")
    print("=" * 60)
    
    dialogs = parse_script(SCRIPT)
    print(f"\n[INFO] Знайдено {len(dialogs)} діалогів:\n")
    
    for i, d in enumerate(dialogs):
        print(f"  {i+1:02d}. {d['speaker']}: {d['text'][:40]}...")
    
    video_path = create_video(dialogs, "test_movie.mp4")
    
    if video_path:
        print(f"\n[SUCCESS] Відео створено: {video_path}")
        print(f"[INFO] Відкрийте файл у плеєрі")
    else:
        print("\n[ERROR] Не вдалося створити відео")

if __name__ == "__main__":
    main()