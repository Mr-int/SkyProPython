import re
from src.reader import CSV_file_read, XLSX_file_read


def find_transactions(transactions, search_term):
    """Поиск операций по заданному запросу."""
    return [trans for trans in transactions if "description" in trans and re.search(search_term, str(trans["description"]))]


def categorize_operations(transactions, category_dict):
    """Подсчет операций по категориям."""
    category_counts = {}
    for trans in transactions:
        if "description" in trans:
            for category, keywords in category_dict.items():
                if any(keyword.lower() in str(trans["description"]).lower() for keyword in keywords):
                    category_counts[category] = category_counts.get(category, 0) + 1
    return category_counts


def process_data():
    """Основная функция обработки данных."""
    csv_transactions = CSV_file_read()
    excel_transactions = CSV_file_read()
    combined_data = csv_transactions + excel_transactions

    search_query = "Перевод"
    matched_transactions = find_transactions(combined_data, search_query)
    print("Обнаруженные операции:")
    print(matched_transactions)

    transaction_categories = {
        "Перевод между картами": ["Перевод с карты на карту"],
        "Перевод организации": ["Перевод организации"],
        "Открытие вклада": ["Открытие вклад"],
        "Перевод между счетами": ["Перевод со счета на счет"]
    }

    counts_by_category = categorize_operations(combined_data, transaction_categories)
    print("\nСтатистика операций по категориям:")
    print(counts_by_category)


if __name__ == "__main__":
    process_data()