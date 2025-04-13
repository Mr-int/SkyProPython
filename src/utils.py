import pandas as pd
import logging

logger = logging.getLogger(__name__)

def read_excel_data(file_path: str) -> list:
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