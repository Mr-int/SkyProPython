import pytest
from src.decorators import log

@log()
def sum_numbers(x, y):
    """
    Функция для сложения двух чисел.
    """
    return x + y

@pytest.mark.parametrize("x, y, result", [
    (1, 2, 3),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_sum_numbers(x, y, result):
    """
    Проверка функции сложения на различных входных данных.
    Убедитесь, что функция sum_numbers возвращает правильные результаты.
    """
    assert sum_numbers(x, y) == result

def test_sum_non_numeric():
    """
    Проверка функции сложения на нечисловых значениях.
    Убедитесь, что функция sum_numbers вызывает TypeError при попытке сложить нечисловые значения.
    """
    with pytest.raises(TypeError):
        sum_numbers("a", 2)

def test_sum_large_numbers():
    """
    Проверка функции сложения на больших числах.
    Убедитесь, что функция sum_numbers правильно обрабатывает большие целые числа.
    """
    assert sum_numbers(1000000, 2000000) == 3000000

def test_sum_negative_numbers():
    """
    Проверка функции сложения на отрицательных числах.
    Убедитесь, что функция sum_numbers правильно обрабатывает отрицательные целые числа.
    """
    assert sum_numbers(-1, -2) == -3

def test_log_error_to_file(tmp_path):
    """
    Проверка логирования в файл при возникновении ошибки.
    Убедитесь, что декоратор log записывает информацию об ошибках в указанный файл.
    """
    log_file = tmp_path / "log.txt"

    @log(filename=str(log_file))
    def divide(x, y):
        """
        Вспомогательная функция для тестирования логирования.
        """
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    with open(log_file, 'r') as file:
        log_data = file.read()
        assert "Function 'divide' started with args: (10, 0), kwargs: {}" in log_data
        assert "Function 'divide' raised an exception: ZeroDivisionError with args: (10, 0), kwargs: {}" in log_data
