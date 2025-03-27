def filter_by_currency(transaction, currency, start=0):
    """ Функция фильтрует транзакции по заданной валюте """
    example = [x.get("operationAmount").get("currency").get("code") for x in transaction]
    if currency not in example:
        while True:
            yield "Данной валюты нет в списке транзакций"
    list_of_currency = list(filter(lambda x: x.get("operationAmount").get("currency").get("code") == currency, transaction))
    while True:
        yield list_of_currency[start]
        start += 1


def transaction_descriptions(transaction, start=0):
    """ Функция возвращает описание операции """
    desciption = [x.get("description") for x in transaction]
    if desciption == []:
        while True:
            yield "Транзакций нет"
    else:
        while True:
            yield desciption[start]
            start += 1


def card_number_generator(start_number, stop_number):
    """ Функция генерирует номера карты """
    for i in range(start_number, stop_number + 1):
        card_number_length = 16
        card_number_length -= len(str(i))

        card_number = f"{'0' * card_number_length}{i}"
        yield f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"


transactions = (
    [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]
)
