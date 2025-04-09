import os

from src.decorators import log


def test_log_console(capsys):
    @log()
    def test_function(x, y):
        return x + y

    print(test_function(1, 3))
    captured = capsys.readouterr()
    assert captured.out == "test_function 4\n"
    print(test_function(1, "4"))
    captured = capsys.readouterr()
    assert captured.out == "test_function error:TypeError. Inputs: (1, '4'), {}\n"


def test_log_file():
    filename = "mylog.txt"

    @log(filename=filename)
    def test_function(x, y):
        return x + y

    test_function(1, 10)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(base_dir, "..", "logs")
    file_path = os.path.join(dir, filename)
    text = open(file_path, "r")
    assert text.read() == "test_function 11"
    test_function(1, "10")
    text = open(file_path, "r")
    assert text.read() == """test_function error:TypeError. Inputs: (1, '10'), {}"""
