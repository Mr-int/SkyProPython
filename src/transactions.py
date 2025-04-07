import csv
import pandas as pd

def reading_csv(csv_data):
    """Читает csv файл"""
    with open(csv_data, encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        return list(reader)


def reading_xlsx(xlsx_data):
    """Читает xlsx файл"""
    exel_data = pd.read_excel(xlsx_data)
    transactions_list = exel_data.to_dict(orient="records")

    return transactions_list