import os
import shutil
from src.command.logger import p_error, p_good


def rm(udal, recursive=False):
    """
    Удаление файлов и каталогов
    udal: что удаляем
    recursive: опция -r для удаления каталогов, требуется подтверждение
    """
    try:
        # Делаем путь абсолютным
        old_dir = os.getcwd()
        if not os.path.isabs(udal):
            udal = os.path.join(old_dir, udal)

        # Проверяем существование удаляемого
        if not os.path.exists(udal):
            print(f"Ошибка: {f"'{udal}' не существует"}")
            p_error(f"'{udal}' не существует")
            return False

        # Защита от удаления чего не надо
        abs_udal = os.path.abspath(udal)
        if abs_udal == "/" or abs_udal.endswith("/.."):
            error_msg = "Запрещено удалять корневой или родительский каталог"
            print(f"Ошибка: {error_msg}")
            p_error(error_msg)
            return False

        # Удаление файла
        if os.path.isfile(udal):
            os.remove(udal)
            print(f"Файл удален: {udal}")
            p_good(f"rm {udal}")
            return True

        # Удаление каталога
        elif os.path.isdir(udal):
            if recursive:  # Опция -r
                confirm = input(f"Удалить каталог '{udal}' и всё его содержимое? (y/n): ")
                if confirm.lower() == 'y':
                    shutil.rmtree(udal)
                    print(f"Каталог удален: {udal}")
                    p_good(f"rm -r {udal}")
                    return True
                else:
                    print("Отменено")
                    p_error("Отменено пользователем")
                    return False
            else:
                print(f"Ошибка: {f"Используйте -r для удаления каталогов"}")
                p_error(f"Используйте -r для удаления каталогов")
                return False

    except PermissionError:
        print(f"Ошибка: {f"Нет прав доступа для удаления"}")
        p_error(f"Нет прав доступа для удаления")
        return False
    except Exception as e:
        print(f"Ошибка: {f"Ошибка при удалении: {e}"}")
        p_error(f"Ошибка при удалении: {e}")
        return False