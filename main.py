import re
from src.external_api import get_amount
from src.generators import filter_by_currency, transaction_descriptions
from src.search_reader import find_transactions
from src.processing import filter_by_state, sort_by_date
from src.reader import CSV_file_read, XLSX_file_read
from src.utils import get_transaction
from src.widget import mask_account_card


def error_message() -> str:
    """Вывод сообщения об ошибке при некорректном вводе."""
    return "Ошибка ввода. Повторите попытку.\n"


def select_file_type():
    """Определение формата входного файла."""
    print("Здравствуйте! Это программа для анализа банковских операций.")
    choice = input(
        """Выберите формат файла:
    1. JSON
    2. CSV
    3. Excel (xlsx/xls)\n"""
    )
    if choice == "1":
        print("Выбран формат JSON.\n")
        return get_transaction('data/operations.json'), "json"
    elif choice == "2":
        print("Выбран формат CSV.\n")
        return CSV_file_read(), "csv"
    elif choice == "3":
        print("Выбран формат Excel.\n")
        return CSV_file_read(), "excel"
    else:
        print(error_message())
        return select_file_type()


def filter_by_status(operations):
    """Фильтрация операций по статусу."""
    print("Выберите статус для фильтрации операций:")
    status_input = input("Доступные статусы: EXECUTED, CANCELED, PENDING\n").upper()
    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    if status_input not in valid_statuses:
        print("Неверный статус. Укажите один из предложенных.")
        return filter_by_status(operations)
    return filter_by_state(operations, status_input)


def sort_by_datetime(operations):
    """Сортировка операций по дате."""
    sort_choice = input("Отсортировать по дате? Да/Нет\n").lower()
    if sort_choice == "да":
        direction = input("По возрастанию (1) или по убыванию (2)?\n")
        if direction == "1":
            return sort_by_date(operations)
        elif direction == "2":
            return sort_by_date(operations, "decreasing")
        else:
            print(error_message())
            return sort_by_datetime(operations)
    elif sort_choice == "нет":
        return operations
    else:
        print(error_message())
        return sort_by_datetime(operations)


def filter_by_rubles(operations, format_type):
    """Фильтрация операций по валюте (рубли)."""
    currency_choice = input("Показать только операции в рублях? Да/Нет\n").lower()
    if currency_choice == "да":
        result = list(filter_by_currency(operations, "RUB"))
        return result
    elif currency_choice == "нет":
        return operations
    else:
        print(error_message())
        return filter_by_rubles(operations, format_type)


def search_by_keyword(operations):
    """Поиск операций по ключевому слову."""
    search_choice = input("Искать по ключевому слову? Да/Нет\n").lower()
    if search_choice == "да":
        keyword = input("Введите слово для поиска:\n")
        return find_transactions(operations, keyword)
    elif search_choice == "нет":
        return operations
    else:
        print(error_message())
        return search_by_keyword(operations)


def run_program():
    """Основная логика программы."""
    transactions, file_format = select_file_type()
    transactions = filter_by_status(transactions)
    transactions = sort_by_datetime(transactions)
    transactions = filter_by_rubles(transactions, file_format)
    transactions = search_by_keyword(transactions)

    print("Обрабатываю данные...")
    if transactions and len(transactions) > 0:
        print(f"Найдено операций: {len(transactions)}\n")
        for trans in transactions:
            print(trans["date"], next(transaction_descriptions(transactions)))
            if "Перевод" in trans["description"]:
                print(f"{mask_account_card(trans['from'])} -> {mask_account_card(trans['to'])}")
            else:
                print(mask_account_card(trans["to"]))
            print(f"Сумма: {get_amount(trans)} руб.\n")
    else:
        print("Операций по заданным фильтрам не найдено.")


if __name__ == "__main__":
    run_program()