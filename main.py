import logging
from pathlib import Path

from src.interface import Interface
from src.logger import setup_logger
from src.reports import ReportGenerator
from src.services import BankService
from src.utils import load_config

def main() -> None:
    """
    Основная функция приложения, которая инициализирует все компоненты
    и запускает основной цикл работы.
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    setup_logger()
    logger = logging.getLogger(__name__)
    
    try:
        config = load_config()

        bank_service = BankService()
        report_generator = ReportGenerator()
        interface = Interface(bank_service, report_generator)

        interface.run()
        
    except Exception as e:
        logger.error(f"Произошла ошибка при выполнении программы: {e}")
        raise

if __name__ == "__main__":
    main()