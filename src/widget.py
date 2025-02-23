from masks import get_mask_account, get_mask_card_number


def mask_account_card(card_data: str) -> str:
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




