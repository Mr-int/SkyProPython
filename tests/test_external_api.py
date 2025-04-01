import os
from unittest.mock import MagicMock, patch

import pytest

from src.external_api import all_amount, get_amount


@pytest.fixture
def mock_env():
    """Фикстура для установки переменных окружения"""
    with patch.dict(os.environ, {"API_KEY": "test_api_key"}):
        yield


@pytest.fixture
def sample_transaction_rub():
    """Фикстура для транзакции в рублях"""
    return {"operationAmount": {"amount": "100.50", "currency": {"code": "RUB"}}}


@pytest.fixture
def sample_transaction_usd():
    """Фикстура для транзакции в долларах"""
    return {"operationAmount": {"amount": "100.50", "currency": {"code": "USD"}}}


def test_get_amount_rub(sample_transaction_rub):
    """Тест для транзакции в рублях"""
    result = get_amount(sample_transaction_rub)
    assert result == 100.50


def test_get_amount_usd(mock_env, sample_transaction_usd):
    """Тест для транзакции в долларах"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 9000.0}

    with patch("requests.get", return_value=mock_response):
        result = get_amount(sample_transaction_usd)
        assert result == 9000.0


def test_get_amount_invalid_data():
    """Тест для невалидных данных транзакции"""
    invalid_transaction = {"invalid": "data"}
    result = get_amount(invalid_transaction)
    assert result is None


def test_all_amount_empty_list():
    """Тест для пустого списка транзакций"""
    result = all_amount([])
    assert result == 0


def test_all_amount_mixed_currencies(mock_env):
    """Тест для списка транзакций с разными валютами"""
    transactions = [
        {"operationAmount": {"amount": "100.50", "currency": {"code": "RUB"}}},
        {"operationAmount": {"amount": "100.50", "currency": {"code": "USD"}}},
    ]

    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 9000.0}

    with patch("requests.get", return_value=mock_response):
        result = all_amount(transactions)
        assert result == 9100.50


def test_all_amount_invalid_transactions():
    """Тест для списка с невалидными транзакциями"""
    transactions = [{"invalid": "data"}, None, []]
    result = all_amount(transactions)
    assert result == 0
