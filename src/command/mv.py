import os
import shutil
from src.command.logger import p_error, p_good



def mv(source, destination):
    """
    Перемещение или переименование файлов/каталогов
    source: что перемещаем
    destination: куда перемещаем
    """
    try:
        # Делаем пути абсолютными
        current_dir = os.getcwd()
        if not os.path.isabs(source):
            source = os.path.join(current_dir, source)
        if not os.path.isabs(destination):
            destination = os.path.join(current_dir, destination)

        # Проверка существования источника
        if not os.path.exists(source):
            print(f"Ошибка: {f"Источник '{source}' не существует"}")
            p_error(f"Источник '{source}' не существует")
            return False

        # Перемещаем файл/каталог
        shutil.move(source, destination)
        print(f"Перемещено: {source} -> {destination}")
        p_good(f"mv {source} {destination}")
        return True

    except PermissionError:
        print(f"Ошибка: {f"Нет прав доступа для перемещения"}")
        p_error(f"Нет прав доступа для перемещения")
        return False
    except Exception as e:
        print(f"Ошибка: {f"Ошибка при перемещении: {e}"}")
        p_error(f"Ошибка при перемещении: {e}")
        return False