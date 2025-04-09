import pytest

from src import masks


@pytest.mark.parametrize(
    "numbers_info,expected",
    [
        ("1596837868705199", "1596 83** **** 5199"),
        ("6831982476737658", "6831 98** **** 7658"),
        ("897304958f7290kj", "Error"),
        ("394075", "Error"),
    ],
)
def test_mask_card_number(numbers_info, expected):
    assert masks.get_mask_card_number(numbers_info) == expected


@pytest.mark.parametrize(
    "numbers,expected",
    [
        ("73654108430135874305", "**4305"),
        ("19861059860492865092", "**5092"),
        ("saigq54298dfgjkh895h", "Error"),
        ("23576908536", "Error"),
    ],
)
def test_get_mask_account(numbers, expected):
    assert masks.get_mask_account(numbers) == expected


def test_exceptions():
    class da:
        def __str__(self):
            raise TypeError

    obj = da()
    assert masks.get_mask_account(obj) == "Error"
    assert masks.get_mask_card_number(obj) == "Error"
