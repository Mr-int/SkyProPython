# Финансовый калькулятор транзакций

Проект для работы с финансовыми транзакциями, включающий функционал чтения JSON-файлов с транзакциями и конвертации валют с использованием внешнего API.

## Функциональность

- Чтение транзакций из JSON-файла
- Конвертация сумм транзакций в рубли
- Поддержка различных валют (RUB, USD, EUR)
- Обработка ошибок и валидация данных

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/SkyProPython.git
cd SkyProPython
```

2. Установите зависимости с помощью Poetry:
```bash
poetry install
```

3. Создайте файл `.env` в корневой директории проекта и добавьте в него API ключ:
```
API_KEY=your_api_key_here
```

## Структура проекта

```
SkyProPython/
├── data/
│   └── operations.json    # Файл с транзакциями
├── src/
│   ├── utils.py          # Утилиты для работы с JSON
│   └── external_api.py   # Работа с внешним API
├── tests/
│   ├── test_utils.py     # Тесты для utils.py
│   └── test_external_api.py  # Тесты для external_api.py
├── .env                  # Файл с переменными окружения
├── pyproject.toml        # Конфигурация Poetry
└── README.md            # Документация проекта
```

## Использование

### Чтение транзакций

```python
from src.utils import get_transaction

# Получение списка транзакций из файла
transactions = get_transaction("data/operations.json")
```

### Конвертация валют

```python
from src.external_api import get_amount, all_amount

# Получение суммы одной транзакции в рублях
amount = get_amount(transaction)

# Получение общей суммы всех транзакций в рублях
total = all_amount(transactions)
```

## Тестирование

Для запуска тестов используйте команду:
```bash
poetry run pytest tests/
```

Тесты покрывают следующие сценарии:
- Чтение пустого файла
- Обработка невалидного JSON
- Проверка формата данных
- Конвертация валют
- Обработка ошибок

## Требования

- Python 3.8+
- Poetry для управления зависимостями
- API ключ от Exchange Rates Data API

## Лицензия

MIT