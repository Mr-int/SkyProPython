from src.transactions import reading_csv, reading_xlsx
print(reading_csv("data/transactions.csv"), "\n")
print(reading_xlsx("data/transactions_excel.xlsx"))