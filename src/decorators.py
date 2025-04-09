import os
from functools import wraps


def log(filename=""):
    """Проверяет функцию на ошибки
    и если в начале дано название файла то записывает лог в файл если нет то выводит в консоль"""

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                if filename == "":
                    return f"{func.__name__} error:{type(e).__name__}. Inputs: {args}, {kwargs}"
                else:
                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    log_dir = os.path.join(base_dir, "..", "logs")
                    log_file_path = os.path.join(log_dir, filename)
                    log_file = open(log_file_path, "w")
                    log_file.write(f"{func.__name__} error:{type(e).__name__}. Inputs: {args}, {kwargs}")
                    log_file.close()
                    return ""
            else:
                if filename == "":
                    return f"{func.__name__} {result}"
                else:
                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    log_dir = os.path.join(base_dir, "..", "logs")
                    log_file_path = os.path.join(log_dir, filename)
                    log_file = open(log_file_path, "w")
                    log_file.write(f"{func.__name__} {result}")
                    log_file.close()
                    return ""

        return inner

    return decorator
