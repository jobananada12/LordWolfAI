"""
LordWolf AI Studio

Project Snapshot Generator

Створює повний текстовий знімок проєкту:
- структуру папок
- усі файли
- статус (порожній/непорожній)
- кількість рядків
- повний вміст файлів
"""

from pathlib import Path

ROOT = Path(__file__).parent.resolve()

OUTPUT = ROOT / "project_snapshot.txt"

IGNORE_DIRS = {
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "env",
    ".pytest_cache",
}

IGNORE_EXT = {
    ".pyc",
    ".pyo",
    ".exe",
    ".dll",
    ".so",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".mp3",
    ".wav",
    ".ogg",
    ".mp4",
    ".avi",
    ".mov",
    ".zip",
    ".7z",
}


def build_tree(path: Path, prefix=""):

    lines = []

    entries = sorted(
        path.iterdir(),
        key=lambda p: (p.is_file(), p.name.lower())
    )

    entries = [
        e for e in entries
        if e.name not in IGNORE_DIRS
    ]

    for index, entry in enumerate(entries):

        last = index == len(entries) - 1

        connector = "└── " if last else "├── "

        lines.append(prefix + connector + entry.name)

        if entry.is_dir():

            extension = "    " if last else "│   "

            lines.extend(
                build_tree(entry, prefix + extension)
            )

    return lines


python_files = []
other_files = []

for file in ROOT.rglob("*"):

    if not file.is_file():
        continue

    if any(part in IGNORE_DIRS for part in file.parts):
        continue

    if file.suffix.lower() in IGNORE_EXT:
        continue

    rel = file.relative_to(ROOT)

    if file.suffix == ".py":
        python_files.append(rel)
    else:
        other_files.append(rel)

python_files.sort()
other_files.sort()

total = 0
filled = 0
empty = 0

with open(OUTPUT, "w", encoding="utf-8") as out:

    out.write("=" * 80 + "\n")
    out.write("LORDWOLF AI STUDIO\n")
    out.write("PROJECT SNAPSHOT\n")
    out.write("=" * 80 + "\n\n")

    out.write("СТРУКТУРА ПРОЄКТУ\n")
    out.write("-" * 80 + "\n")

    out.write(ROOT.name + "\n")

    for line in build_tree(ROOT):
        out.write(line + "\n")

    out.write("\n\n")

    files = python_files + other_files

    for rel in files:

        total += 1

        full = ROOT / rel

        text = ""

        try:

            text = full.read_text(
                encoding="utf-8",
                errors="replace"
            )

        except Exception as e:

            text = f"<<Помилка читання: {e}>>"

        rows = len(text.splitlines())

        status = "НЕ ПУСТИЙ"

        if text.strip() == "":
            status = "ПУСТИЙ"
            empty += 1
        else:
            filled += 1

        out.write("=" * 80 + "\n")
        out.write(f"Файл: {rel.as_posix()}\n")
        out.write("=" * 80 + "\n")
        out.write(f"Статус : {status}\n")
        out.write(f"Рядків : {rows}\n")
        out.write("-" * 80 + "\n")
        out.write("ВМІСТ ФАЙЛУ\n")
        out.write("-" * 80 + "\n")

        if text.strip():
            out.write(text)
        else:
            out.write("(порожній файл)")

        out.write("\n\n")

    out.write("=" * 80 + "\n")
    out.write("СТАТИСТИКА\n")
    out.write("=" * 80 + "\n")
    out.write(f"Всього файлів : {total}\n")
    out.write(f"Заповнених    : {filled}\n")
    out.write(f"Порожніх      : {empty}\n")

print()
print("========================================")
print("Project snapshot створено успішно.")
print(f"Файл: {OUTPUT}")
print("========================================")