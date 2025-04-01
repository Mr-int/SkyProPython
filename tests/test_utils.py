import json
import os
from unittest.mock import mock_open, patch

import pytest

from src.utils import get_transaction


def test_get_transaction_empty_file():
    """Тест для пустого файла"""
    with patch("builtins.open", mock_open(read_data="")):
        result = get_transaction("path/to/file.json")
        assert result == []


def test_get_transaction_invalid_json():
    """Тест для невалидного JSON"""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        result = get_transaction("path/to/file.json")
        assert result == []


def test_get_transaction_not_list():
    """Тест для JSON, который не является списком"""
    with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
        result = get_transaction("path/to/file.json")
        assert result == []


def test_get_transaction_valid_data():
    """Тест для валидных данных"""
    test_data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
        result = get_transaction("path/to/file.json")
        assert result == test_data


def test_get_transaction_file_not_found():
    """Тест для несуществующего файла"""
    with patch("os.path.isfile", return_value=False):
        result = get_transaction("nonexistent.json")
        assert result == []
