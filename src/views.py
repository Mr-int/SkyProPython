import logging
import os
import re
import requests
from datetime import datetime
from dotenv import load_dotenv
import json
import pandas as pd
from src.utils import read_excel_data

load_dotenv()

EXCHANGE_API_KEY = os.getenv('EXCHANGE_API_KEY')
STOCK_API_KEY = os.getenv('STOCK_API_KEY')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(PROJECT_ROOT, 'data')
LOGS_FOLDER = os.path.join(PROJECT_ROOT, 'logs')
USER_CONFIG_PATH = os.path.join(DATA_FOLDER, 'user_config.json')
TRANSACTIONS_PATH = os.path.join(DATA_FOLDER, 'operations.xlsx')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_file = os.path.join(LOGS_FOLDER, 'app.log')
file_handler = logging.FileHandler(log_file)
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def get_time_greeting(current_time: str) -> str:
    """
    Возвращает приветствие в зависимости от времени суток.
    """
    try:
        logger.debug("Обработка времени: %s", current_time)
        time_obj = datetime.strptime(current_time, "%H:%M:%S")
        
        greetings = {
            (0, 6): "Доброй ночи!",
            (6, 12): "Доброе утро!",
            (12, 18): "Добрый день!",
            (18, 24): "Добрый вечер!"
        }
        
        for (start, end), greeting in greetings.items():
            if start <= time_obj.hour < end:
                return greeting
                
        return "Доброй ночи!"
        
    except Exception as e:
        logger.error(f"Ошибка при определении приветствия: {e}")
        return "Приветствие не определено"

def analyze_card_transactions(transactions: list[dict]) -> list[dict]:
    """
    Анализирует транзакции по картам и рассчитывает кэшбэк.
    """
    card_analysis = {}
    card_pattern = re.compile(r"\*\d{4}")

    for transaction in transactions:
        if isinstance(transaction["Номер карты"], str) and card_pattern.fullmatch(transaction["Номер карты"]):
            if "Сумма операции" in transaction and "Статус" in transaction:
                card_number = transaction["Номер карты"][1:]
                amount = transaction["Сумма операции"]

                if transaction["Статус"] == "OK" and float(amount) < 0:
                    if card_number not in card_analysis:
                        card_analysis[card_number] = 0.0
                    card_analysis[card_number] += abs(float(amount))

    results = []
    for card_num, total in card_analysis.items():
        cashback = total * 0.01
        results.append({
            "card_number": card_num,
            "total_spent": round(total, 2),
            "cashback_amount": round(cashback, 2)
        })

    return results

def get_largest_transactions(transactions: list[dict], limit: int = 5) -> list[dict]:
    """
    Находит самые крупные транзакции.
    """
    expenses = [
        transaction for transaction in transactions
        if "Сумма операции" in transaction and transaction["Сумма операции"] < 0
    ]

    top_transactions = sorted(expenses, key=lambda x: abs(x["Сумма операции"]), reverse=True)[:limit]
    
    formatted_transactions = []
    for transaction in top_transactions:
        try:
            date_str = transaction["Дата операции"]
            date_obj = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
            
            formatted_transactions.append({
                "transaction_date": date_obj.strftime("%Y-%m-%d"),
                "amount": round(abs(transaction["Сумма операции"]), 2),
                "category": transaction["Категория"],
                "description": transaction["Описание"]
            })
        except (ValueError, KeyError) as e:
            logger.error(f"Ошибка при обработке транзакции: {e}")

    return formatted_transactions

def fetch_exchange_rates() -> dict:
    """
    Получает актуальные курсы валют.
    """
    rates = {}
    currencies = ["USD", "EUR"]
    
    for currency in currencies:
        url = f"https://open.er-api.com/v6/latest/{currency}"
        headers = {"apikey": EXCHANGE_API_KEY}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if "rates" in data and "RUB" in data["rates"]:
                rates[currency] = round(float(data["rates"]["RUB"]), 2)
    
    if not rates:
        logger.error("Не удалось получить курсы валют")
    
    return rates

def get_stock_prices(stock_list: list) -> list:
    """
    Получает текущие цены акций.
    """
    stock_prices = []
    
    for ticker in stock_list:
        api_url = f"https://api.api-ninjas.com/v1/stockprice?ticker={ticker}"
        response = requests.get(api_url, headers={"X-Api-Key": STOCK_API_KEY})
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and "price" in data:
                stock_prices.append({
                    "symbol": ticker,
                    "current_price": data["price"]
                })
            else:
                logger.warning(f"Не удалось получить цену для акции {ticker}")
    
    return stock_prices

def display_interface():
    """
    Основная функция отображения интерфейса.
    """
    transactions = read_excel_data(TRANSACTIONS_PATH)
    
    with open(USER_CONFIG_PATH, 'r') as f:
        user_config = json.load(f)
    
    current_time = datetime.now().strftime('%d.%m.%Y %H:%M')
    print(f"Текущее время: {current_time}")
    
    analysis_results = process_financial_data(transactions)
    results = json.loads(analysis_results)
    
    print("\nАнализ карт:")
    for card in results["cards"]:
        print(f"Карта: ****{card['card_number']}")
        print(f"Расходы: {card['total_spent']} RUB")
        print(f"Кэшбэк: {card['cashback_amount']} RUB")
    
    print("\nКрупнейшие транзакции:")
    for transaction in results["transactions"]:
        print(f"Дата: {transaction['transaction_date']}")
        print(f"Сумма: {transaction['amount']} RUB")
        print(f"Категория: {transaction['category']}")
        print(f"Описание: {transaction['description']}\n")
    
    print("\nКурсы валют:")
    for currency, rate in results["exchange_rates"].items():
        print(f"{currency}: {rate} RUB")
    
    if "stock_portfolio" in user_config:
        print("\nПортфель акций:")
        stocks = get_stock_prices(user_config["stock_portfolio"])
        for stock in stocks:
            print(f"- {stock['symbol']}: {stock['current_price']} USD")

def process_financial_data(data: list) -> str:
    """
    Обрабатывает финансовые данные.
    """
    greeting = get_time_greeting(datetime.now().strftime("%H:%M:%S"))
    card_analysis = analyze_card_transactions(data)
    top_transactions = get_largest_transactions(data)
    exchange_rates = fetch_exchange_rates()
    
    with open(USER_CONFIG_PATH, 'r') as f:
        user_config = json.load(f)
    
    stock_data = get_stock_prices(user_config.get("stock_portfolio", []))
    
    response = {
        "greeting": greeting,
        "cards": card_analysis,
        "transactions": top_transactions,
        "exchange_rates": exchange_rates,
        "stocks": stock_data
    }
    
    return json.dumps(response, ensure_ascii=False, indent=2)
