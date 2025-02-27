from typing import Union


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
