def log(filename=None):
    """
    Функция записывает информацию, включая переданные аргументы и результаты.
    Если указано имя файла, записывает это в файл если не указан, то выводится в консоль.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            log_msg = f"Function '{func.__name__}' started with args: {args}, kwargs: {kwargs}\n"

            try:
                result = func(*args, **kwargs)
                log_msg += f"Function '{func.__name__}' finished successfully with: {result}\n"
                if filename:
                    with open(filename, 'a') as f:
                        f.write(log_msg)
                else:
                    print(log_msg)
                return result

            except Exception as e:
                log_msg += f"Function '{func.__name__}' raised an exception: {type(e).__name__} with args: {args}, kwargs: {kwargs}\n"
                if filename:
                    with open(filename, 'a') as f:
                        f.write(log_msg)
                else:
                    print(log_msg)
                raise

        return wrapper

    return decorator


@log()
def add(a, b):
    return a + b


add(2, 3)