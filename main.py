from src.command.logger import p_info
from src.command.ls import ls
from src.command.cd import cd
from src.command.cat import cat
from src.command.cp import cp
from src.command.mv import mv
from src.command.rm import rm
import os
from logging import basicConfig, DEBUG

basicConfig(
    level = DEBUG,
    filename ="shell.log",
    format = '%(asctime)s - [%(levelname)s] - %(message)s'
)
def main():
    print("=== Терминал ===")
    print("Доступные команды: ls, cd, cat, cp, mv, rm, by")
    print("Чтобы выйди введите 'by'")
    print("=" * 30)

    while True:
        try:
            path = os.getcwd()
            command = input(f'{path} >> ').strip()
            if not command:
                continue
            parts = command.split()
            cmd_name = parts[0].lower()
            p_info(command)


            if cmd_name == "by":
                print("Конец")
                break

            elif cmd_name == "ls":
                if len(parts) > 1:
                    args = parts[1]
                else:
                    args = ""
                ls(path, args)

            elif cmd_name == "cd":
                if len(parts) > 1:
                    path = cd(parts[1])
                else:
                    path = cd()
                cd(path)

            elif cmd_name == "cat":
                if len(parts) > 1:
                    file_path = parts[1]
                    cat(file_path)
                else:
                    print("Ошибка: укажите путь к файлу")

            elif cmd_name == "cp":
                if len(parts) >= 3:
                    if parts[1] == "-r":
                        if len(parts) >= 4:
                            source = parts[2]
                            destination = parts[3]
                            cp(source, destination, recursive=True)
                        else:
                            print("Ошибка: укажите источник и назначение")
                    else:
                        source = parts[1]
                        destination = parts[2]
                        cp(source, destination)

            elif cmd_name == "mv":
                if len(parts) >= 3:
                    source = parts[1]
                    destination = parts[2]
                    mv(source, destination)
                else:
                    print("Ошибка: укажите источник и назначение")

            elif cmd_name == "rm":
                if len(parts) >= 2:
                    if parts[1] == "-r":
                        if len(parts) >= 3:
                            rm(parts[2], recursive=True)
                        else:
                            print("Ошибка: укажите что удалять")
                    else:
                        rm(parts[1])
                else:
                    print("Ошибка: укажите что удалять")

            else:
                print(f"Неизвестная команда: {cmd_name}")

        except KeyboardInterrupt:
            print("\nПока")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()


