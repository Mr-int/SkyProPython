import pytest

from src.widget import mask_account_card, get_date


@pytest.mark.parametrize(
    "variable, result",
    [
        ("Visa MasterCard 1888776545162708", "Visa MasterCard 1888 77** **** 2708"),
        ("MirPay SBP 1234567891234567", "MirPay SBP 1234 56** **** 4567"),
        ("", "Ошибка, проверьте введенные данные"),
        (" ", "Ошибка, проверьте введенные данные"),
        ("MirPay SBP 123467", "Ошибка, проверьте введенные данные"),
    ],
)
def test_mask_account_card(variable, result):
    assert mask_account_card(variable) == result


@pytest.mark.parametrize(
    "date, exptected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2027-05-12T02:26:18.671407", "12.05.2027"),
        ("2024-05-1202:26:18.671407", "Ошибка даты"),
        ("", "Ошибка даты"),
        (" ", "Ошибка даты"),
    ],
)
def test_get_date(date, exptected):
    assert get_date(date) == exptected
