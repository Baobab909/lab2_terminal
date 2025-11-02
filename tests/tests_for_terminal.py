import os
import tempfile
import shutil
import pytest
from unittest.mock import patch
from io import StringIO
from src.command.ls import ls
from src.command.cd import cd
from src.command.cat import cat
from src.command.cp import cp
from src.command.mv import mv
from src.command.rm import rm


class TestTerminalCommands:
    """Основные тесты для команд терминала"""

    def setup_method(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        # Создаем тестовые файлы
        with open('test_file.txt', 'w') as f:
            f.write('Hello, World!')

        os.makedirs('test_dir', exist_ok=True)
        with open('test_dir/nested.txt', 'w') as f:
            f.write('Nested content')


    # Тесты для ls
    def test_ls_basic(self):
        """Тест базового вывода ls"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            ls(self.test_dir)
            output = mock_stdout.getvalue()
            assert 'test_file.txt' in output
            assert 'test_dir' in output

    def test_ls_nonexistent_path(self):
        """Тест ls с несуществующим путем"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            ls('/nonexistent/path')
            output = mock_stdout.getvalue()
            assert 'не найден' in output

    # Тесты для cd
    def test_cd_basic(self):
        """Тест перехода в директорию"""
        new_path = cd('test_dir')
        assert os.path.basename(new_path) == 'test_dir'

    def test_cd_nonexistent(self):
        """Тест перехода в несуществующую директорию"""
        original_dir = os.getcwd()
        new_path = cd('nonexistent_dir')
        assert new_path == original_dir

    def test_cd_home(self):
        """Тест перехода в домашнюю директорию"""
        home_dir = os.path.expanduser("~")
        new_path = cd('~')
        assert new_path == home_dir

    # Тесты для cat
    def test_cat_basic(self):
        """Тест вывода содержимого файла"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = cat('test_file.txt')
            output = mock_stdout.getvalue()
            assert result is True
            assert 'Hello, World!' in output

    def test_cat_nonexistent(self):
        """Тест вывода несуществующего файла"""
        result = cat('nonexistent.txt')
        assert result is False

    def test_cat_directory(self):
        """Тест вывода директории вместо файла"""
        result = cat('test_dir')
        assert result is False

    # Тесты для cp
    def test_cp_file(self):
        """Тест копирования файла"""
        result = cp('test_file.txt', 'copied.txt')
        assert result is True
        assert os.path.exists('copied.txt')

    def test_cp_directory_without_r(self):
        """Тест копирования директории без -r"""
        result = cp('test_dir', 'copied_dir')
        assert result is False

    def test_cp_directory_with_r(self):
        """Тест копирования директории с -r"""
        result = cp('test_dir', 'copied_dir', recursive=True)
        assert result is True
        assert os.path.exists('copied_dir/nested.txt')

    # Тесты для mv
    def test_mv_file(self):
        """Тест перемещения файла"""
        result = mv('test_file.txt', 'moved.txt')
        assert result is True
        assert os.path.exists('moved.txt')
        assert not os.path.exists('test_file.txt')

    def test_mv_nonexistent(self):
        """Тест перемещения несуществующего файла"""
        result = mv('nonexistent.txt', 'moved.txt')
        assert result is False

    # Тесты для rm
    def test_rm_file(self):
        """Тест удаления файла"""
        result = rm('test_file.txt')
        assert result is True
        assert not os.path.exists('test_file.txt')

    def test_rm_directory_without_r(self):
        """Тест удаления директории без -r"""
        result = rm('test_dir')
        assert result is False

    def test_rm_directory_with_r_confirmed(self, monkeypatch):
        """Тест удаления директории с подтверждением"""
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        result = rm('test_dir', recursive=True)
        assert result is True
        assert not os.path.exists('test_dir')

    def test_rm_directory_with_r_cancelled(self, monkeypatch):
        """Тест удаления директории с отменой"""
        monkeypatch.setattr('builtins.input', lambda _: 'n')
        result = rm('test_dir', recursive=True)
        assert result is False
        assert os.path.exists('test_dir')


class TestMainProgram:
    """Тесты основного цикла программы"""

    @patch('builtins.input')
    def test_main_exit(self, mock_input):
        """Тест выхода из программы"""
        from main import main
        mock_input.side_effect = ['by']

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            try:
                main()
            except SystemExit:
                pass
            output = mock_stdout.getvalue()
            assert 'Конец' in output

    @patch('builtins.input')
    def test_unknown_command(self, mock_input):
        """Тест неизвестной команды"""
        from main import main
        mock_input.side_effect = ['unknown_cmd', 'by']

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            try:
                main()
            except SystemExit:
                pass
            output = mock_stdout.getvalue()
            assert 'Неизвестная команда' in output

    def test_keyboard_interrupt(self):
        """Тест прерывания программы"""
        from main import main

        with patch('builtins.input') as mock_input:
            mock_input.side_effect = KeyboardInterrupt()

            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                try:
                    main()
                except SystemExit:
                    pass
                output = mock_stdout.getvalue()
                assert 'Пока' in output


def test_edge_cases():
    """Тесты граничных случаев"""

    # Создаем временную директорию
    test_dir = tempfile.mkdtemp()
    original_dir = os.getcwd()

    try:
        os.chdir(test_dir)

        # Тест пустых команд
        from main import main
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ['', ' ', 'by']
            with patch('sys.stdout', new_callable=StringIO):
                try:
                    main()
                except SystemExit:
                    pass

        # Тест ls с опцией -l
        with open('test.txt', 'w') as f:
            f.write('test')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            ls(test_dir, '-l')
            output = mock_stdout.getvalue()
            assert 'test.txt' in output

        # Тест cd без аргументов (должен перейти в домашнюю директорию)
        home_dir = os.path.expanduser("~")
        result_path = cd()
        assert result_path == home_dir

    finally:
        os.chdir(original_dir)
        shutil.rmtree(test_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])