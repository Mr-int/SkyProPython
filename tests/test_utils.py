import os
from pathlib import Path
from typing import List

import pandas as pd
import pytest

from src.utils import load_config, read_excel_data


@pytest.fixture
def sample_excel_file(tmp_path: Path) -> str:
    """
    Создает временный Excel файл для тестирования.
    """
    df = pd.DataFrame({
        'Номер карты': ['*1234', '*5678'],
        'Сумма операции': [1000, -500],
        'Статус': ['OK', 'OK']
    })
    file_path = tmp_path / "test.xlsx"
    df.to_excel(file_path, index=False)
    return str(file_path)


def test_read_excel_data_success(sample_excel_file: str) -> None:
    """
    Тест успешного чтения Excel файла.
    """
    result = read_excel_data(sample_excel_file)
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, dict) for item in result)
    assert all('Номер карты' in item for item in result)


def test_read_excel_data_file_not_found() -> None:
    """Тест чтения несуществующего файла."""
    result = read_excel_data("nonexistent.xlsx")
    assert isinstance(result, list)
    assert len(result) == 0


def test_load_config(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Тест загрузки конфигурации.
    """
    # Подменяем переменные окружения для теста
    env_vars = {
        'API_KEY': 'test_key',
        'API_URL': 'http://test.com',
        'DEBUG': 'true',
        'LOG_LEVEL': 'DEBUG',
        'DATA_DIR': './test_data',
        'REPORT_DIR': './test_reports'
    }
    
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    
    config = load_config()
    
    assert config['api_key'] == 'test_key'
    assert config['api_url'] == 'http://test.com'
    assert config['debug'] is True
    assert config['log_level'] == 'DEBUG'
    assert config['data_dir'] == './test_data'
    assert config['report_dir'] == './test_reports'
    
    # Проверяем создание директорий
    assert Path(config['data_dir']).exists()
    assert Path(config['report_dir']).exists()


def test_xlsx_reader(tmp_path):
    """Тест на корректное чтение нормального файла"""
    df = pd.DataFrame({
        "Номер карты": ["1234567890123456", "6543210987654321"],
        "Имя": ["Иван", "Мария"]
    })
    test_file = os.path.join(tmp_path, "test.xlsx")
    df.to_excel(test_file, index=False)

    result = xlsx_reader(test_file)

    assert len(result) == 2
    assert result[0]["Номер карты"] == "1234567890123456"
    assert result[1]["Имя"] == "Мария"


def test_xlsx_reader_card_numbers(tmp_path):
    """Тест на преобразование числовых номеров карт в строки"""
    df = pd.DataFrame({
        "Номер карты": [1234567890123456, 9876543210987654],
        "Имя": ["Алексей", "Ольга"]
    })
    test_file = os.path.join(tmp_path, "testik.xlsx")
    df.to_excel(test_file, index=False)

    result = xlsx_reader(test_file)
    assert result[0]["Номер карты"] == "1234567890123456"
    assert result[1]["Номер карты"] == "9876543210987654"


