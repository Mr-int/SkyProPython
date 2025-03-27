from typing import Union

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_data: Union[str]) -> str:
    """Обрабатывает информацию как о картах, так и о счетах
    Возвращает строку с замаскированным номером"""
    card_data = card_data.strip()

    if len(card_data) < 16:
        return "Ошибка, проверьте введенные данные"

    count = 0
    for i in card_data:
        if i.isdigit():
            first_digit = count
        else:
            count += 1

    if "Счет" in card_data:
        mask_card_data = get_mask_account(card_data[first_digit::])
        if mask_card_data[0].isalpha():
            return "Ошибка, проверьте введенные данные"
        else:
            mask_card_data = card_data[:first_digit] + mask_card_data
    else:
        mask_card_data = get_mask_card_number(card_data[first_digit::])
        if mask_card_data[0].isalpha():
            return "Ошибка, проверьте введенные данные"
        else:
            mask_card_data = card_data[:first_digit] + mask_card_data

    return mask_card_data


def get_date(date: str) -> str:
    """функция принимает на вход строку с датой в формате
    2024-03-11T02:26:18.671407  и возвращает строку с датой в формате ДД.ММ.ГГГГ"""
    try:
        index = date.index("T")
        date = date[:index]
        date_array = date.split("-")
        date_reforming = ".".join(reversed(date_array))
    except:
        return "Ошибка даты"
    else:
        return date_reforming
