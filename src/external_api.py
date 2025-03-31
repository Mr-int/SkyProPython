import os

import requests
from dotenv import load_dotenv

API_KEY = os.getenv("API_KEY")


def get_amount(data_transaction):
    try:
        money_type = data_transaction["operationAmount"]["currency"]["code"]
        amount = float(data_transaction["operationAmount"]["amount"])

        currency = "RUB"

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={currency}&from={money_type}&amount={amount}"

        headers = {"apikey": API_KEY}
        response = requests.get(url, headers=headers)
        result = response.json()
    except (KeyError, TypeError, ValueError):
        return None


def all_amount(dict_transaction):
    count = 0
    for i in dict_transaction:
        try:
            if not isinstance(i, dict) or not i:
                continue

            if i["operationAmount"]["currency"]["code"] == "RUB":
                count += float(i["operationAmount"]["amount"])
            else:
                converted = get_amount(i)
                if converted is not None:
                    count += converted

        except (KeyError, TypeError, ValueError):
            continue
    return count
