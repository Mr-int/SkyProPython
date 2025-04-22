import logging
import os
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def read_excel_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные из Excel файла и преобразует их в список словарей.
    """
    try:
        df = pd.read_excel(file_path)
        if not df.empty and "Номер карты" in df.columns:
            df["Номер карты"] = df["Номер карты"].astype(str)
            logger.info(f"Успешно прочитан файл {file_path}")
            return df.to_dict("records")
        else:
            logger.warning(f"Файл {file_path} пуст или не содержит необходимых колонок")
            return []
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {str(e)}")
        return []


def load_config() -> Dict[str, Any]:
    """
    Загружает конфигурацию из .env файла.
    """
    load_dotenv()
    
    config = {
        'api_key': os.getenv('API_KEY'),
        'api_url': os.getenv('API_URL'),
        'debug': os.getenv('DEBUG', 'False').lower() == 'true',
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'data_dir': os.getenv('DATA_DIR', './data'),
        'report_dir': os.getenv('REPORT_DIR', './reports')
    }
    
    # Создаем необходимые директории
    Path(config['data_dir']).mkdir(exist_ok=True)
    Path(config['report_dir']).mkdir(exist_ok=True)
    
    return config