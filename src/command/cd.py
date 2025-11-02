import os
from src.command.logger import p_error


def cd(path=""):
    """
    Переход в указанный каталог
    path: путь к каталогу (относительный или абсолютный)
    Возвращает новую текущую директорию, поддерживает ~ и ..
    """
    try:
        old_dir = os.getcwd() # текущая директория

        if not path:
            new_path = os.path.expanduser("~")
        else:
            if path == "..":
                # Переход на уровень выше
                new_path = os.path.dirname(old_dir)
            elif path == "~":
                # Переход в домашний каталог
                new_path = os.path.expanduser("~")
            else:
                # Обычный путь
                if os.path.isabs(path):
                    new_path = path
                else:
                    new_path = os.path.join(old_dir, path)
        new_path = os.path.abspath(new_path)

        # Проверка существования каталога
        if not os.path.exists(new_path):
            print(f"Ошибка: {f"Каталог '{new_path}' не существует"}")
            p_error(f"Каталог '{new_path}' не существует")
            return old_dir  # Возвращаем старую директорию

        if not os.path.isdir(new_path):
            print(f"Ошибка: {f"'{new_path}' не является каталогом"}")
            p_error(f"'{new_path}' не является каталогом")
            return old_dir

        # Меняем текущий каталог
        os.chdir(new_path)

        return new_path  # Возвращаем новую директорию

    except PermissionError:
        print(f"Ошибка: {f"Нет прав доступа к каталогу '{path}'"}")
        p_error(f"Нет прав доступа к каталогу '{path}'")
        return os.getcwd()
    except Exception as e:
        print(f"Ошибка: {f"Ошибка при переходе в каталог: {e}"}")
        p_error(f"Ошибка при переходе в каталог: {e}")
        return os.getcwd()