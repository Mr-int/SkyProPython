import os
from datetime import datetime
from typing import List, Dict, Any

from src import files_reader, generator, processing, utils, widget, collection


def display_welcome_message() -> None:
    print("=" * 50)
    print("Банковский Аналитик v2.0")
    print("=" * 50)
    print("\nВыберите источник данных для анализа:")
    print("1. JSON файл с транзакциями")
    print("2. CSV файл с транзакциями")
    print("3. Excel файл с транзакциями")
    print("4. Выход")


def get_file_type() -> int:
    while True:
        try:
            choice = int(input("\nВаш выбор: "))
            if choice in [1, 2, 3, 4]:
                return choice
            print("Пожалуйста, выберите число от 1 до 4")
        except ValueError:
            print("Введите корректное число")


def get_filter_options() -> Dict[str, Any]:
    options = {}
    
    print("\nНастройка фильтров:")
    print("-" * 30)
    
    # Статус транзакции
    while True:
        print("\nВыберите статус транзакции:")
        print("1. EXECUTED (Выполнено)")
        print("2. CANCELED (Отменено)")
        print("3. PENDING (В обработке)")
        status_choice = input("Ваш выбор (1-3): ")
        status_map = {"1": "EXECUTED", "2": "CANCELED", "3": "PENDING"}
        if status_choice in status_map:
            options["status"] = status_map[status_choice]
            break
        print("Неверный выбор. Попробуйте снова.")
    
    # Сортировка по дате
    print("\nСортировать по дате?")
    if input("(Да/Нет): ").lower() == "да":
        print("1. По возрастанию")
        print("2. По убыванию")
        sort_choice = input("Ваш выбор (1-2): ")
        options["sort_date"] = True
        options["sort_desc"] = sort_choice == "2"
    
    # Фильтр по валюте
    print("\nФильтровать по валюте?")
    if input("(Да/Нет): ").lower() == "да":
        print("Введите код валюты (например, RUB, USD, EUR):")
        options["currency"] = input().upper()
    
    # Фильтр по описанию
    print("\nФильтровать по ключевому слову в описании?")
    if input("(Да/Нет): ").lower() == "да":
        options["keyword"] = input("Введите ключевое слово: ")
    
    return options


def process_transactions(file_type: int, options: Dict[str, Any]) -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    # Загрузка данных
    if file_type == 1:
        file_path = os.path.join(data_dir, "operations.json")
        transactions = utils.get_transaction(file_path)
    elif file_type == 2:
        file_path = os.path.join(data_dir, "transactions.csv")
        transactions = files_reader.CSV_file_read(file_path)
    else:
        file_path = os.path.join(data_dir, "transactions_excel.xlsx")
        transactions = files_reader.XLSX_file_read(file_path)
    
    # Применение фильтров
    if transactions:
        # Фильтр по статусу
        transactions = processing.filter_by_state(transactions, options["status"])
        
        # Сортировка по дате
        if options.get("sort_date"):
            transactions = processing.sort_by_date(transactions, options["sort_desc"])
        
        # Фильтр по валюте
        if options.get("currency"):
            if file_type == 1:
                transactions = generator.filter_by_currency_json(transactions, options["currency"])
            else:
                transactions = generator.filter_by_currency_csvxlsx(transactions, options["currency"])
        
        # Фильтр по ключевому слову
        if options.get("keyword"):
            transactions = collection.description_filter(transactions, options["keyword"])
        
        display_results(transactions, file_type)
    else:
        print("\nНе найдено транзакций, соответствующих заданным критериям.")


def display_results(transactions: List[Dict], file_type: int) -> None:
    print("\n" + "=" * 50)
    print(f"Найдено транзакций: {len(transactions)}")
    print("=" * 50 + "\n")
    
    for transaction in transactions:
        print(f"Дата: {widget.get_date(transaction['date'])}")
        print(f"Описание: {transaction['description']}")
        
        if transaction['description'] == "Открытие вклада":
            print(f"Получатель: {widget.mask_account_card(transaction['to'])}")
        else:
            print(f"Отправитель: {widget.mask_account_card(transaction['from'])}")
            print(f"Получатель: {widget.mask_account_card(transaction['to'])}")
        
        if file_type == 1:
            amount = transaction['operationAmount']['amount']
            currency = transaction['operationAmount']['currency']['name']
        else:
            amount = transaction['amount']
            currency = transaction['currency_name']
        
        print(f"Сумма: {round(float(amount))} {currency}")
        print("-" * 50)


def main():
    while True:
        display_welcome_message()
        choice = get_file_type()
        
        if choice == 4:
            print("\nСпасибо за использование программы. До свидания!")
            break
        
        options = get_filter_options()
        process_transactions(choice, options)
        
        print("\nХотите выполнить новый анализ?")
        if input("(Да/Нет): ").lower() != "да":
            print("\nСпасибо за использование программы. До свидания!")
            break


if __name__ == "__main__":
    main()
