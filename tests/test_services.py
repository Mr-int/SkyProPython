import json
from pathlib import Path
from typing import Dict, List

import pandas as pd
import pytest

from src.services import search_transactions_from_excel


@pytest.fixture
def sample_transactions_file(tmp_path: Path) -> str:
    """
    Создает временный файл с тестовыми транзакциями.
    """
    transactions = pd.DataFrame({
        'Описание': ['Покупка продуктов', 'Оплата такси', 'Перевод'],
        'Категория': ['Продукты', 'Транспорт', 'Переводы'],
        'Сумма': [-1000, -500, -2000]
    })
    
    file_path = tmp_path / "operations.xlsx"
    transactions.to_excel(file_path, index=False)
    return str(file_path)


def test_search_transactions_by_description(sample_transactions_file: str) -> None:
    """
    Тест поиска транзакций по описанию.
    """
    result = search_transactions_from_excel("продукт")
    assert result is not None
    
    transactions = json.loads(result)
    assert len(transactions) == 1
    assert transactions[0]['Описание'] == 'Покупка продуктов'
    assert transactions[0]['Категория'] == 'Продукты'


def test_search_transactions_by_category(sample_transactions_file: str) -> None:
    """
    Тест поиска транзакций по категории.
    """
    result = search_transactions_from_excel("транспорт")
    assert result is not None
    
    transactions = json.loads(result)
    assert len(transactions) == 1
    assert transactions[0]['Описание'] == 'Оплата такси'
    assert transactions[0]['Категория'] == 'Транспорт'


def test_search_transactions_no_results(sample_transactions_file: str) -> None:
    """
    Тест поиска транзакций без результатов.
    """
    result = search_transactions_from_excel("несуществующая категория")
    assert result is not None
    
    transactions = json.loads(result)
    assert len(transactions) == 0


def test_search_transactions_file_not_found() -> None:
    """Тест поиска транзакций при отсутствии файла."""
    result = search_transactions_from_excel("test")
    assert result is None

