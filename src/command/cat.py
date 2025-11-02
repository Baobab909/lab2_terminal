import os
from src.command.logger import p_error, p_good


def cat(file_path):
    """
    Вывод содержимого файла в консоль
    file_path: путь к файлу (относительный или абсолютный)
    """
    try:
        # Если путь не абсолютный, делаем его абсолютным
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.getcwd(), file_path)

        # Проверка на существование
        if not os.path.exists(file_path):
            print(f"Ошибка: {f"Файл '{file_path}' не существует"}")
            p_error(f"Файл '{file_path}' не существует")
            return False

        # Проверка на файл
        if os.path.isdir(file_path):
            print(f"Ошибка: {f"'{file_path}' является каталогом, а не файлом"}")
            p_error(f"'{file_path}' является каталогом, а не файлом")
            return False

        # Вывод содержимого
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)

        # Логируем успешность
        p_good(f"cat {file_path}")
        return True

    except PermissionError:
        print(f"Ошибка: {f"Нет прав доступа к файлу '{file_path}'"}")
        p_error(f"Нет прав доступа к файлу '{file_path}'")
        return False
    except UnicodeDecodeError:
        print(f"Ошибка: {f"Файл '{file_path}' содержит бинарные данные или не поддерживаемую кодировку"}")
        p_error(f"Файл '{file_path}' содержит бинарные данные или не поддерживаемую кодировку")
        return False
    except Exception as e:
        print(f"Ошибка: {f"Ошибка при чтении файла: {e}"}")
        p_error(f"Ошибка при чтении файла: {e}")
        return False