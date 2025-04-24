from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import pytest

from src.reports import spending_by_category, read_excel_safe, report_to_file


@pytest.fixture
def sample_transactions_file(tmp_path: Path) -> str:
    """
    Создает временный файл с тестовыми транзакциями.
    """
    current_date = datetime.now()
    transactions = pd.DataFrame({
        'Дата операции': [
            current_date - timedelta(days=i) 
            for i in range(5)
        ],
        'Сумма операции': [-1000, -500, -750, -1200, -300],
        'Категория': ['Продукты'] * 5
    })
    
    transactions['Дата операции'] = transactions['Дата операции'].dt.strftime('%d.%m.%Y %H:%M:%S')
    
    file_path = tmp_path / "transactions.xlsx"
    transactions.to_excel(file_path, index=False)
    return str(file_path)


def test_spending_by_category(sample_transactions_file: str) -> None:
    """
    Тест анализа трат по категории.
    """
    df = pd.read_excel(sample_transactions_file)

    result = spending_by_category(df, 'Продукты')
    
    assert not result.empty
    assert result.iloc[0]['Категория'] == 'Продукты'
    assert result.iloc[0]['Потрачено'] == 3750  # Сумма всех транзакций за последние 90 дней


def test_spending_by_category_with_date(sample_transactions_file: str) -> None:
    """
    Тест анализа трат по категории с указанной датой.
    """
    df = pd.read_excel(sample_transactions_file)
    current_date = datetime.now()
    date_str = current_date.strftime('%d.%m.%Y')
    
    result = spending_by_category(df, 'Продукты', date_str)
    
    assert not result.empty
    assert result.iloc[0]['Категория'] == 'Продукты'
    assert result.iloc[0]['Потрачено'] == 3750


def test_spending_by_category_no_transactions(sample_transactions_file: str) -> None:
    """
    Тест анализа трат по несуществующей категории.
    """
    df = pd.read_excel(sample_transactions_file)
    
    result = spending_by_category(df, 'Несуществующая категория')
    
    assert not result.empty
    assert result.iloc[0]['Категория'] == 'Несуществующая категория'
    assert result.iloc[0]['Потрачено'] == 0


def test_read_excel_safe(tmp_path):
    file_path = tmp_path / "test.xlsx"
    data = {
        'Дата операции': ['01.01.2024 00:00:00'],
        'Сумма операции': [-100.0],
        'Категория': ['Еда']
    }
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)

    result = read_excel_safe(file_path)

    assert not result.empty
    assert result.shape == (1, 3)

def test_report_to_file_dir_not_found(tmp_path, capsys):
    @report_to_file("test")
    def test_func():
        return pd.DataFrame({
            'Категория': ['Еда'],
            'Потрачено': [100.0],
            'Период': ['01.01.2024 - 01.01.2024']
        })

    test_func()

    captured = capsys.readouterr()
    assert "Директория logs не найдена" not in captured.out


