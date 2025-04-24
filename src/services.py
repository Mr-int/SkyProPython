import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BankService:
    """
    Класс для работы с банковскими операциями.
    """
    def __init__(self):
        self.data_path = Path(__file__).parent.parent / "data" / "operations.xlsx"
        self.logger = logging.getLogger(__name__)
        
    def search_transactions(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """
        Поиск транзакций по описанию или категории.
        """
        try:
            df = pd.read_excel(self.data_path)
            query = query.lower()
            
            result_df = df[
                (df['Описание'].str.contains(query, case=False, na=False)) |
                (df['Категория'].str.contains(query, case=False, na=False))
            ]
            
            return result_df.to_dict(orient='records')
            
        except Exception as e:
            self.logger.error(f"Ошибка при поиске транзакций: {e}")
            return None
            
    def get_transaction_history(self) -> Optional[pd.DataFrame]:
        """
        Получает историю всех транзакций.
        """
        try:
            return pd.read_excel(self.data_path)
        except Exception as e:
            self.logger.error(f"Ошибка при чтении истории транзакций: {e}")
            return None

def main_services():
    """
    Главная функция для поиска транзакций и возврата JSON-ответа.
    """
    query = input("Введите категорию или описание для поиска: ")
    bank_service = BankService()
    result = bank_service.search_transactions(query)
    print(result)


