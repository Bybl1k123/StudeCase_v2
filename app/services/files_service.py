"""Сервис для работы с файлами."""
import os
import sys
import platform
import subprocess
import shutil

# Определяем базовую директорию (рядом с .exe или корень проекта)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

STORAGE_DIR = os.path.join(BASE_DIR, "uploads")


def open_external_file(file_path: str) -> bool:
    if not file_path or not os.path.exists(file_path):
        return False

    # Обработка для Android
    if platform.system() == "Android" or "ANDROID_ARGUMENT" in os.environ:
        try:
            import flet as ft
            # Пытаемся открыть файл через системный Intent Android
            # Важно: используем абсолютный путь
            abs_path = os.path.abspath(file_path)
            ft.launch_url(f"file://{abs_path}")
            return True
        except Exception as e:
            print(f"Ошибка открытия файла на Android: {e}")
            return False

    # Обработка для Windows, macOS и Linux (остается как было)
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":
            subprocess.call(("open", file_path))
        else:
            subprocess.call(("xdg-open", file_path))
        return True
    except Exception:
        return False


def detect_file_type(filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext in ("png", "jpg", "jpeg", "gif", "webp", "bmp"):
        return "image"
    if ext == "pdf":
        return "pdf"
    if ext in ("doc", "docx", "odt", "rtf"):
        return "doc"
    if ext in ("txt", "md"):
        return "note"
    return "file"


def human_size(num_bytes: int) -> str:
    if num_bytes < 1024:
        return f"{num_bytes} Б"
    if num_bytes < 1024 * 1024:
        return f"{num_bytes / 1024:.1f} КБ"
    return f"{num_bytes / (1024 * 1024):.1f} МБ"


def copy_to_storage(src_path: str) -> str:
    os.makedirs(STORAGE_DIR, exist_ok=True)
    name = os.path.basename(src_path)
    dest = os.path.join(STORAGE_DIR, name)
    base, ext = os.path.splitext(name)
    counter = 1
    while os.path.exists(dest):
        dest = os.path.join(STORAGE_DIR, f"{base}_{counter}{ext}")
        counter += 1
    shutil.copy2(src_path, dest)
    return dest


def delete_stored_file(file_path: str) -> bool:
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
            return True
        except Exception:
            return False
    return True
