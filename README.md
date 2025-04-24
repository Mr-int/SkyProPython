# Финансовый Анализатор

Проект для анализа финансовых операций, отслеживания курсов валют и мониторинга акций.

## Функциональность

- Анализ транзакций по банковским картам
- Расчет кэшбэка
- Отслеживание крупнейших транзакций
- Мониторинг курсов валют
- Отслеживание цен акций

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/financial-analyzer.git
cd financial-analyzer
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` и добавьте необходимые API ключи:
```
EXCHANGE_API_KEY=your_exchange_api_key_here
STOCK_API_KEY=your_stock_api_key_here
```

## Использование

1. Поместите файл с транзакциями в формате Excel в папку `data/`
2. Настройте конфигурацию пользователя в файле `data/user_config.json`
3. Запустите приложение:
```bash
python main.py
```

## Структура проекта

```
.
├── data/               
├── logs/            
├── src/               
│   ├── __init__.py   
│   ├── interface.py  
│   ├── utils.py      
│   ├── logger.py    
│   ├── reports.py   
│   ├── services.py   
│   └── views.py
├── tests/           
│   ├── init.py   
│   ├── test_reports.py   
│   ├── test_services.py   
│   ├── test_utils.py   
│   ├── test_views.py   
├── main.py            
└── requirements.txt   
```

## Требования

- Python 3.8+
- pandas
- python-dotenv
- requests

## Лицензия

MIT
