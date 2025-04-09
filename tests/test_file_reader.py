from unittest.mock import patch

import pandas as pd

from src import files_reader


@patch("pandas.read_csv")
def test_CSV_file_read_patch(mock_get):
    data = {"id": ["1", "2", "3"], "amount": ["452", "3453", "1420"], "currency_code": ["USD", "RUB", "USD"]}
    df = pd.DataFrame(data)
    mock_get.return_value = df
    assert files_reader.CSV_file_read("..\\tests\\data_test\\transactions.csv") == [
        {"id": "1", "amount": "452", "currency_code": "USD"},
        {"id": "2", "amount": "3453", "currency_code": "RUB"},
        {"id": "3", "amount": "1420", "currency_code": "USD"},
    ]
    mock_get.assert_called_once_with("..\\tests\\data_test\\transactions.csv", delimiter=";")


def test_CSV_file_read():
    assert files_reader.CSV_file_read("psorjtgrsij") == "Файл не найден"


@patch("pandas.read_excel")
def test_XLSX_file_read_patch(mock_get):
    data = {"id": ["1", "2", "3"], "amount": ["452", "3453", "1420"], "currency_code": ["USD", "RUB", "USD"]}
    df = pd.DataFrame(data)
    mock_get.return_value = df
    assert files_reader.XLSX_file_read("..\\tests\\data_test\\transactions_excel.xlsx") == [
        {"id": "1", "amount": "452", "currency_code": "USD"},
        {"id": "2", "amount": "3453", "currency_code": "RUB"},
        {"id": "3", "amount": "1420", "currency_code": "USD"},
    ]
    mock_get.assert_called_once_with("..\\tests\\data_test\\transactions_excel.xlsx")


def test_XLSX_file_read():
    assert files_reader.XLSX_file_read("psorjtgrsij") == "Файл не найден"
