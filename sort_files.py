import os
import shutil
import logging
import asyncio
from pathlib import Path

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Асинхронна функція для читання файлів з папки
async def read_folder(source_folder, output_folder):
    source_folder = Path(source_folder)
    output_folder = Path(output_folder)

    if not source_folder.exists() or not source_folder.is_dir():
        logging.error(f"Вихідна папка {source_folder} не існує або не є директорією.")
        return

    if not output_folder.exists():
        logging.info(f"Цільова папка {output_folder} не існує. Створюю...")
        output_folder.mkdir(parents=True)
        logging.info(f"Цільова папка {output_folder} успішно створена.")

    tasks = []

    # Рекурсивне прочитання файлів
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            tasks.append(copy_file(Path(root) / file, output_folder))

    await asyncio.gather(*tasks)

# Асинхронна функція для копіювання файлів
async def copy_file(file_path, output_folder):
    try:
        ext = file_path.suffix.lower()[1:]  # Отримуємо розширення файлу
        if not ext:
            return  # Якщо розширення немає, пропускаємо файл

        # Створюємо підпапку для конкретного розширення
        destination_folder = output_folder / ext
        destination_folder.mkdir(parents=True, exist_ok=True)

        # Визначаємо цільовий шлях файлу
        destination_file = destination_folder / file_path.name

        # Копіюємо файл
        shutil.copy2(file_path, destination_file)
        logging.info(f"Файл {file_path} успішно скопійовано до {destination_file}")

    except Exception as e:
        logging.error(f"Помилка при копіюванні файлу {file_path}: {e}")

# Головна функція для обробки введення користувача та запуску
def main():
    source_folder = input("Введіть шлях до вихідної папки: ").strip()
    output_folder = input("Введіть шлях до цільової папки: ").strip()

    # Запуск асинхронної функції
    asyncio.run(read_folder(source_folder, output_folder))

if __name__ == "__main__":
    main()
