import os
from src.command.logger import p_error, p_good
from datetime import datetime
import stat

def ls(path, arg=False):
    """
    Отображение списка файлов в текущем рабочем каталоге
    :param path: путь к каталогу (относительный или абсолютный)
    :param arg: опция -l для подробного отображения
    """
    try:
        if not os.path.exists(path):
            print('Ошибка: путь', path, 'не найден')
            p_error('Путь не найден')
            return
        fails = os.listdir(path)
        fails.sort()

        for i in fails:
            full = os.path.join(path, i)
            if arg:
                info_f = os.stat(full)
                size_f = info_f.st_size
                time_f = datetime.fromtimestamp(info_f.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                mode_f = os.stat(path).st_mode
                itog_f = stat.filemode(mode_f)
                print(f'{itog_f} {size_f} {time_f} {i}')
            else:
                print(i)

        p_good(f"ls {arg if arg else ''}")

    except Exception as e:
        print(f'Ошибка: {e}')
        p_error(f"Ошибка при выполнении ls: {e}")







