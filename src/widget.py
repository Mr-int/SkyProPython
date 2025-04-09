from src import masks


def mask_account_card(card_inf: str) -> str:
    """Обрабатывает информацию как о картах, так и о счетах
    Возвращает строку с замаскированным номером"""
    index = 0
    card_inf = str(card_inf)
    for character in card_inf:
        if character.isdigit():
            break
        else:
            index += 1
    if card_inf[index - 1] != " ":
        return "Error"
    if card_inf[: index - 1] == "Счет":
        if len(card_inf[index:]) == 20 and card_inf[index:].isdigit():
            return card_inf[: index - 1] + " " + masks.get_mask_account(card_inf[index:])
        else:
            return "Error"
    else:
        if len(card_inf[index:]) == 16 and card_inf[index:].isdigit():
            return card_inf[: index - 1] + " " + masks.get_mask_card_number(card_inf[index:])
        else:
            return "Error"


def get_date(date: str) -> str:
    """Функция, которая принимает на вход строку с датой в формате
    "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ" """
    year, month, day = date[:10].split("-")
    if year.isdigit() and month.isdigit() and day.isdigit():
        return f"{day}.{month}.{year}"
    else:
        return "Error"
