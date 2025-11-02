import os
import shutil
from src.command.logger import p_error, p_good


def cp(source, destination, recursive=False):
    """
    Копирование из источника в назначение
    source: что копируем
    destination: куда копируем
    recursive: опция -r для копирования каталогов
    """
    try:
        # Абсолютные пути
        old_dir = os.getcwd()
        if not os.path.isabs(source):
            source = os.path.join(old_dir, source)
        if not os.path.isabs(destination):
            destination = os.path.join(old_dir, destination)

        # Есть ли источник
        if not os.path.exists(source):
            print(f"Ошибка: {f"Источник '{source}' не существует"}")
            p_error(f"Источник '{source}' не существует")
            return False

        # Копирование файла
        if os.path.isfile(source):
            shutil.copy2(source, destination)
            print(f"Файл скопирован: {source} -> {destination}")
            p_good(f"cp {source} {destination}")
            return True

        # Копирование каталога
        elif os.path.isdir(source):
            if recursive:  # Опция -r
                shutil.copytree(source, destination)
                print(f"Каталог скопирован: {source} -> {destination}")
                p_good(f"cp -r {source} {destination}")
                return True
            else:
                print(f"Ошибка: {f"Используйте -r для копирования каталогов"}")
                p_error(f"Используйте -r для копирования каталогов")
                return False

    except PermissionError:
        print(f"Ошибка: {f"Нет прав доступа"}")
        p_error(f"Нет прав доступа")
        return False
    except Exception as e:
        print(f"Ошибка: {f"Ошибка при копировании: {e}"}")
        p_error(f"Ошибка при копировании: {e}")
        return False