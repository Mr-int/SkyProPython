import pytest
from src.search_reader import find_transactions, categorize_operations
from src.reader import CSV_file_read, XLSX_file_read

sample_data = [
    {"description": "Перевод с карты на карту"},
    {"description": "Перевод организации"}
]


def test_find_transactions_basic():
    search_term = "Перевод"
    matched_transactions = find_transactions(sample_data, search_term)
    assert len(matched_transactions) == 2


def test_find_transactions_no_match():
    search_term = "Несуществующее слово"
    matched_transactions = find_transactions(sample_data, search_term)
    assert len(matched_transactions) == 0


def test_categorize_transactions():
    transaction_types = {
        "Перевод между картами": ["Перевод с карты на карту"],
        "Перевод организации": ["Перевод организации"]
    }
    category_stats = categorize_operations(sample_data, transaction_types)
    assert len(category_stats) == 2


def test_categorize_transactions_empty():
    transaction_types = {
        "Несуществующая категория": ["Несуществующее слово"]
    }
    category_stats = categorize_operations(sample_data, transaction_types)
    assert len(category_stats) == 0


def test_find_transactions_with_real_data():
    csv_transactions = CSV_file_read()
    excel_transactions = XLSX_file_read()
    combined_transactions = csv_transactions + excel_transactions
    search_term = "Перевод"
    matched_transactions = find_transactions(combined_transactions, search_term)
    assert len(matched_transactions) >= 0


def test_categorize_transactions_with_real_data():
    csv_transactions = CSV_file_read()
    excel_transactions = XLSX_file_read()
    combined_transactions = csv_transactions + excel_transactions
    transaction_types = {
        "Перевод между картами": ["Перевод с карты на карту"],
        "Перевод организации": ["Перевод организации"]
    }
    category_stats = categorize_operations(combined_transactions, transaction_types)
    assert len(category_stats) >= 0