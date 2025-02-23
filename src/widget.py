from typing import Union

from masks import get_mask_account, get_mask_card_number


def mask_account_card(card_data: Union[str]) -> str:
    """Обрабатывает информацию как о картах, так и о счетах
    Возвращает строку с замаскированным номером"""
    card_data = card_data.strip()
    count = 0
    for i in card_data:
        if i.isdigit():
            first_digit = count
        else:
            count += 1

    if "Счет" in card_data:
        mask_card_data = card_data[:first_digit] + get_mask_account(
            card_data[first_digit::]
        )
    else:
        mask_card_data = card_data[:first_digit] + get_mask_card_number(
            card_data[first_digit::]
        )

    return mask_card_data


def get_date(date: str) -> str:
    """функция принимает на вход строку с датой в формате
    2024-03-11T02:26:18.671407  и возвращает строку с датой в формате ДД.ММ.ГГГГ"""
    index = date.index("T")
    date = date[:index]
    date_array = date.split("-")

    date_reforming = ".".join(reversed(date_array))

    return date_reforming
