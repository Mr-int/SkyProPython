from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Optional, TypeVar

import pandas as pd

T = TypeVar('T')


def report_to_file(filename: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Декоратор для записи отчетов в существующую директорию logs.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args, **kwargs) -> T:
            result = func(*args, **kwargs)

            try:
                logs_dir = Path(__file__).parent.parent / "logs"

                if not logs_dir.is_dir():
                    print(f"Директория logs не найдена по пути: {logs_dir}")
                    return result

                log_file = logs_dir / f"{filename}.log"

                if isinstance(result, pd.DataFrame) and not result.empty:
                    log_entry = (
                        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n"
                        f"Категория: {result.iloc[0]['Категория']}\n"
                        f"Сумма: {float(result.iloc[0]['Потрачено']):.2f} руб.\n"
                        f"Период: {result.iloc[0]['Период']}\n"
                        f"{'-' * 40}\n"
                    )

                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(log_entry)

            except Exception as e:
                print(f"Ошибка записи лога: {e}")

            return result
        return wrapper
    return decorator


@report_to_file("spending")
def spending_by_category(
    transactions: pd.DataFrame,
    category: str,
    date: Optional[str] = None
) -> pd.DataFrame:
    """
    Анализ трат по категории.
    """
    try:
        end_date = datetime.strptime(date, "%d.%m.%Y") if date else datetime.now()
        start_date = end_date - timedelta(days=90)

        transactions['Дата операции'] = pd.to_datetime(
            transactions['Дата операции'],
            format='%d.%m.%Y %H:%M:%S',
            errors='coerce'
        )

        mask = (
            (transactions['Категория'] == category) &
            (transactions['Дата операции'] >= start_date) &
            (transactions['Дата операции'] <= end_date) &
            (transactions['Сумма операции'] < 0)
        )

        filtered = transactions.loc[mask]
        total = abs(filtered['Сумма операции'].sum())

        return pd.DataFrame({
            'Категория': [category],
            'Потрачено': [total],
            'Период': [f"{start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}"]
        })
    except Exception as e:
        print(f"Ошибка анализа: {e}")
        return pd.DataFrame()


def read_excel_safe(file_path: str) -> Optional[pd.DataFrame]:
    """
    Безопасное чтение Excel-файла с проверкой формата.
    """
    try:
        return pd.read_excel(file_path, engine='openpyxl')
    except Exception:
        try:
            return pd.read_excel(file_path, engine='xlrd')
        except Exception as e:
            print(f'Ошибка чтения файла: {e}')
            return None


def main_reports() -> None:
    """
    Основная функция для генерации отчетов.
    """
    file_path = Path(__file__).parent.parent / "data" / "operations.xlsx"
    df = read_excel_safe(str(file_path))

    if df is None:
        print("Не удалось прочитать файл с операциями")
        return

    required = ['Дата операции', 'Сумма операции', 'Категория']
    missing = [col for col in required if col not in df.columns]
    if missing:
        print(f"Доступные колонки: {', '.join(df.columns)}")
        return

    categories = df['Категория'].unique()
    print("\nДоступные категории:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")

    while True:
        try:
            choice = input("\nВведите номер категории: ")
            if not choice.isdigit():
                print("Введите число!")
                continue
            choice = int(choice)
            if 1 <= choice <= len(categories):
                break
            print(f"Введите число от 1 до {len(categories)}")
        except Exception as e:
            print(f"Ошибка ввода: {e}")

    category = categories[choice - 1]
    report = spending_by_category(df, category)

    if not report.empty:
        print("\nРезультат:")
        print(f"Категория: {report.iloc[0]['Категория']}")
        print(f"Потрачено: {report.iloc[0]['Потрачено']:.2f} руб.")
        print(f"Период: {report.iloc[0]['Период']}")


class ReportGenerator:
    """
    Класс для генерации финансовых отчетов.
    """
    def __init__(self):
        self.data_path = Path(__file__).parent.parent / "data" / "operations.xlsx"
        
    def generate_spending_report(self, category: str, date: Optional[str] = None) -> pd.DataFrame:
        """
        Генерирует отчет о тратах по категории.
        
        Args:
            category: Категория для анализа
            date: Дата окончания периода анализа (опционально)
            
        Returns:
            DataFrame с результатами анализа
        """
        df = read_excel_safe(str(self.data_path))
        if df is not None:
            return spending_by_category(df, category, date)
        return pd.DataFrame()
        
    def get_available_categories(self) -> list:
        """
        Возвращает список доступных категорий.
        
        Returns:
            Список категорий
        """
        df = read_excel_safe(str(self.data_path))
        if df is not None and 'Категория' in df.columns:
            return df['Категория'].unique().tolist()
        return []
