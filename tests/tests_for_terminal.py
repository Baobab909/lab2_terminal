import os
import tempfile
import pytest
from unittest.mock import patch
from io import StringIO
from src.command.ls import ls
from src.command.cd import cd
from src.command.cat import cat
from src.command.cp import cp
from src.command.mv import mv
from src.command.rm import rm


class Test:
    """Простые тесты для всех команд терминала"""

    def setup_method(self):
        """Тестовая среда"""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        with open('file1.txt', 'w') as f:
            f.write('content1')
        with open('file2.txt', 'w') as f:
            f.write('content2')
        os.makedirs('dir1')
        os.makedirs('dir2')
        with open('dir1/nested.txt', 'w') as f:
            f.write('nested content')

    # ls
    def test_ls(self):
        """файлы и папки"""
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            ls('.')
            output = mock_out.getvalue()
            assert 'file1.txt' in output
            assert 'dir1' in output

    def test_ls_option(self):
        """детали"""
        with patch('sys.stdout', new_callable=StringIO):
            ls('.', '-l')

    def test_ls_none(self):
        """ls с несуществующим путем"""
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            ls('/bad/path')
            assert 'не найден' in mock_out.getvalue()

    # cd
    def test_cd_valid_directory(self):
        """переходит в существующую папку"""
        new_path = cd('dir1')
        assert 'dir1' in new_path

    def test_cd_none(self):
        """с несуществующей папкой"""
        old = os.getcwd()
        new_path = cd('bad_dir')
        assert new_path == old

    def test_cd_home(self):
        """cd ~"""
        new_path = cd('~')
        assert os.path.exists(new_path)

    def test_cd_empty(self):
        """cd без аргументов"""
        new_path = cd()
        assert os.path.exists(new_path)

    # cat
    def test_cat(self):
        """cat читает файл"""
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            result = cat('file1.txt')
            assert result is True
            assert 'content1' in mock_out.getvalue()

    def test_cat_none(self):
        """cat несуществующего файла"""
        result = cat('bad_file.txt')
        assert result is False

    def test_cat_prava(self):
        """cat с ошибкой прав доступа"""
        with patch('builtins.open', side_effect=PermissionError):
            result = cat('file1.txt')
            assert result is False

    # cp
    def test_cp(self):
        """cp копирует файл"""
        result = cp('file1.txt', 'copy.txt')
        assert result is True
        assert os.path.exists('copy.txt')

    def test_cp_directory(self):
        """cp папки без -r"""
        result = cp('dir1', 'copy_dir')
        assert result is False

    def test_cp_r(self):
        """cp папки с -r"""
        result = cp('dir1', 'copy_dir', recursive=True)
        assert result is True
        assert os.path.exists('copy_dir/nested.txt')

    def test_cp_nonexistent_source(self):
        """cp несуществующего файла"""
        result = cp('bad.txt', 'dest.txt')
        assert result is False

    # mv
    def test_mv(self):
        """mv перемещает файл"""
        result = mv('file1.txt', 'moved.txt')
        assert result is True
        assert not os.path.exists('file1.txt')
        assert os.path.exists('moved.txt')

    def test_mv_directory(self):
        """mv перемещает папку"""
        result = mv('dir1', 'moved_dir')
        assert result is True
        assert not os.path.exists('dir1')
        assert os.path.exists('moved_dir/nested.txt')

    def test_mv_none(self):
        """mv несуществующего файла"""
        result = mv('bad.txt', 'dest.txt')
        assert result is False

    # rm
    def test_rm(self):
        """rm удаляет файл"""
        result = rm('file1.txt')
        assert result is True
        assert not os.path.exists('file1.txt')

    def test_rm_directory(self):
        """rm папки без -r"""
        result = rm('dir1')
        assert result is False
        assert os.path.exists('dir1')

    def test_rm_r(self):
        """rm папки с -r и подтверждением"""
        with patch('builtins.input', return_value='y'):
            result = rm('dir1', recursive=True)
            assert result is True
            assert not os.path.exists('dir1')

    def test_rm_d_r(self):
        """rm папки с -r и отменой"""
        with patch('builtins.input', return_value='n'):
            result = rm('dir1', recursive=True)
            assert result is False
            assert os.path.exists('dir1')

    def test_rm_none(self):
        """rm несуществующего файла"""
        result = rm('bad.txt')
        assert result is False


class TestMain:
    """Тесты основной программы"""

    @patch('builtins.input')
    def test_error(self, mock_input):
        """Неизвестная команда"""
        from main import main
        mock_input.side_effect = ['unknown_cmd', 'by']

        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            try:
                main()
            except SystemExit:
                pass
            assert 'Неизвестная команда' in mock_out.getvalue()

    @patch('builtins.input')
    def test_main_empty_input(self, mock_input):
        """Пустой ввод в main"""
        from main import main
        mock_input.side_effect = ['', 'by']

        with patch('sys.stdout', new_callable=StringIO):
            try:
                main()
            except SystemExit:
                pass



def test_logger():
    """Тесты функций логирования"""
    from src.command.logger import p_error, p_info, p_good

    # Просто проверяем что не падают
    p_error("test error")
    p_info("test info")
    p_good("test command")


if __name__ == "__main__":
    pytest.main()