from logging import error, info

def p_error(msg: str) -> None:
    """
     Сообщение об ошибке и запись в лог
    :param msg: текст сообщения
    """
    error(msg)
    print("Error: " + msg)

def p_info(msg: str) -> None:
    """
    Записывает сообщение в лог
    :param msg: текст сообщения
    """

def p_good(cmd:str) -> None:
    """
    Делает запись в лог об успешном выполнении команды
    :param cmd: имя команды
    """
    info(f"{cmd}: command performed")