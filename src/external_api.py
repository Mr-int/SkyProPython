import os

import requests
from dotenv import load_dotenv


def get_transaction_amount(transaction_info, currency="RUB"):
    """Принимает на вход банковскую операцию и код валюты(по умолчанию RUB) и возвращает сумму транзакции в нужной валюте"""
    code = transaction_info.get("operationAmount").get("currency").get("code")
    amount = transaction_info.get("operationAmount").get("amount")
    if code == currency:
        return amount
    else:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={currency}&from={code}&amount={amount}"
        load_dotenv()
        API_KEY = os.getenv("API_KEY")
        headers = {"apikey": f"{API_KEY}"}
        response = requests.get(url, headers=headers)
        return response.json().get("result")
