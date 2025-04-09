import logging
import os

logger = logging.getLogger("masks")
logger.setLevel(logging.INFO)
base_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(base_dir, "..", "logs")
log_file_path = os.path.join(log_dir, "masks.log")
file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты по правилу XXXX XX** **** XXXX."""
    try:
        card_number_str = str(card_number)
        logger.info("Проверяем номер карты на наличие букв")
        for i in card_number_str:
            if i.isalpha():
                logger.error(f"Некорректный номер карты: {card_number_str}")
                return "Error"
        logger.info("Проверка на нужную длину строки")
        if len(card_number_str) == 16:
            return f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"
        else:
            logger.error("Некорректная длина номера карты")
            return "Error"
    except Exception as ex:
        logger.error(f"Произошла ошибка: {ex}")
        return "Error"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета по правилу **XXXX."""
    try:
        account_number_str = str(account_number)
        logger.info("Проверка на длину строки и на наличие букв в номере счёта")
        if not account_number_str.isdigit():
            logger.error("Некорректный номер счета, есть символы кроме цифр")
            return "Error"
        else:
            if len(account_number_str) == 20:
                return "**" + account_number_str[-4:]
            else:
                logger.error("Некорректная длина счёта")
                return "Error"
    except Exception as ex:
        logger.error(f"Произошла ошибка: {ex}")
        return "Error"
