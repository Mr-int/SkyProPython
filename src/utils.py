import json
import logging
import os

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
base_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(base_dir, "..", "logs")
os.makedirs(log_dir, exist_ok=True)  # Создаем директорию, если она не существует
log_file_path = os.path.join(log_dir, "utils.log")
file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_transaction(json_file_path):
    """Принимает путь до json файла и выводит его списком"""
    logger.info("Проверка что файл есть на пути")
    try:
        if os.path.exists(json_file_path):
            with open(json_file_path, "r", encoding="utf-8") as file:
                logger.info("Открываем и читаем файл")
                transactions = json.load(file)
                logger.info("Проверка что файл имеет нужный тип")
                if isinstance(transactions, list):
                    return transactions
        else:
            logger.error(f"Файл по пути {json_file_path} не существует")
            return []
    except (json.JSONDecodeError, TypeError):
        logger.error("Ошибка при чтении json файла")
        return []
