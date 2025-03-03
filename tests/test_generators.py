import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.mark.parametrize(
    "currency, result",
    [
        (
            "USD",
            [
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                    "operationAmount": {
                        "amount": "9824.07",
                        "currency": {"name": "USD", "code": "USD"},
                    },
                    "description": "Перевод организации",
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                },
                {
                    "id": 142264268,
                    "state": "EXECUTED",
                    "date": "2019-04-04T23:20:05.206878",
                    "operationAmount": {
                        "amount": "79114.93",
                        "currency": {"name": "USD", "code": "USD"},
                    },
                    "description": "Перевод со счета на счет",
                    "from": "Счет 19708645243227258542",
                    "to": "Счет 75651667383060284188",
                },
            ],
        ),
        (
            "RUB",
            [
                {
                    "id": 873106923,
                    "state": "EXECUTED",
                    "date": "2019-03-23T01:09:46.296404",
                    "operationAmount": {
                        "amount": "43318.34",
                        "currency": {"name": "руб.", "code": "RUB"},
                    },
                    "description": "Перевод со счета на счет",
                    "from": "Счет 44812258784861134719",
                    "to": "Счет 74489636417521191160",
                },
                {
                    "id": 594226727,
                    "state": "CANCELED",
                    "date": "2018-09-12T21:27:25.241689",
                    "operationAmount": {
                        "amount": "67314.70",
                        "currency": {"name": "руб.", "code": "RUB"},
                    },
                    "description": "Перевод организации",
                    "from": "Visa Platinum 1246377376343588",
                    "to": "Счет 14211924144426031657",
                },
            ],
        ),
    ],
)
def test_filter_by_currency(transactions, error_filter_by_currency, currency, result):
    filter_by_cur = filter_by_currency(transactions, currency)
    output = []
    for _ in range(2):
        output.append(next(filter_by_cur))
    assert output == result
    assert next(filter_by_currency(transactions, "abc")) == error_filter_by_currency
    assert next(filter_by_currency([], "RUB")) == error_filter_by_currency


def test_transaction_descriptions(transactions, error_transaction_descriptions):
    descriptions = transaction_descriptions(transactions)
    output = []
    for _ in range(5):
        output.append(next(descriptions))
    assert output == ['Перевод организации', 'Перевод со счета на счет', 'Перевод со счета на счет',
                      'Перевод с карты на карту', 'Перевод организации']
    descriptions = transaction_descriptions([])
    assert next(descriptions) == error_transaction_descriptions


def test_card_number_generator():
    output = []
    for card_number in card_number_generator(1, 5):
        output.append(card_number)
    assert output == ['0000 0000 0000 0001', '0000 0000 0000 0002', '0000 0000 0000 0003', '0000 0000 0000 0004',
                      '0000 0000 0000 0005']
    output = []
    for card_number in card_number_generator(9999999999999993, 9999999999999999):
        output.append(card_number)
    assert output == ['9999 9999 9999 9993', '9999 9999 9999 9994', '9999 9999 9999 9995', '9999 9999 9999 9996', '9999 9999 9999 9997', '9999 9999 9999 9998',
                      '9999 9999 9999 9999']