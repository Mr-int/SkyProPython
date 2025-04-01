from typing import Union
from .logger_config import setup_logger

logger = setup_logger('masks')

def get_mask_card_number(card_number: Union[int, str]) -> str:
    """ " Эта функция скрывает номер карты"""
    card_number = str(card_number)
    card_number = card_number.replace(" ", "")

    if len(card_number) != 16:
        return "Некорректный номер карты, пожалуйста введите верный номер карты"

    for i in card_number:
        if i.isdigit():
            pass
        else:
            return "Некорректный номер карты, пожалуйста введите верный номер карты"

    part_1 = card_number[0:4]
    part_2 = card_number[4:6]
    part_3 = card_number[-4::]
    mask_card_number = f"{part_1} {part_2}** **** {part_3}"

    return mask_card_number


def get_mask_account(card_accaunt: Union[int, str]) -> str:
    """Маскирует номер счета"""
    card_accaunt = str(card_accaunt)
    card_accaunt = card_accaunt.strip()

    if len(card_accaunt) < 20:
        return "Некорректный номер счета"

    for i in card_accaunt:
        if i.isdigit():
            pass
        else:
            return "Некорректный номер счета"

    mask_card_accaunt = "**" + card_accaunt[-4::]

    return mask_card_accaunt

def mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты, оставляя видимыми только первые 6 и последние 4 цифры
    
    Args:
        card_number (str): Номер карты
        
    Returns
        str: Замаскированный номер карты
    """
    logger.info(f"Маскирование номера карты: {card_number}")
    
    try:
        # Удаляем все пробелы из номера карты
        card_number = card_number.replace(" ", "")
        
        # Проверяем длину номера карты
        if len(card_number) != 16:
            logger.warning(f"Некорректная длина номера карты: {len(card_number)}")
            return card_number
            
        # Маскируем номер карты
        masked_number = f"{card_number[:6]} ****** {card_number[-4:]}"
        logger.info(f"Номер карты успешно замаскирован: {masked_number}")
        return masked_number
        
    except Exception as e:
        logger.error(f"Ошибка при маскировании номера карты: {str(e)}")
        return card_number

def mask_account_number(account_number: str) -> str:
    """
    Маскирует номер счета, оставляя видимыми только последние 4 цифры
    
    Args:
        account_number (str): Номер счета
        
    Returns:
        str: Замаскированный номер счета
    """
    logger.info(f"Маскирование номера счета: {account_number}")
    
    try:
        # Удаляем все пробелы из номера счета
        account_number = account_number.replace(" ", "")
        
        # Проверяем длину номера счета
        if len(account_number) < 4:
            logger.warning(f"Некорректная длина номера счета: {len(account_number)}")
            return account_number
            
        # Маскируем номер счета
        masked_number = f"**{account_number[-4:]}"
        logger.info(f"Номер счета успешно замаскирован: {masked_number}")
        return masked_number
        
    except Exception as e:
        logger.error(f"Ошибка при маскировании номера счета: {str(e)}")
        return account_number
