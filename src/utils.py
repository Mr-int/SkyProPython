import json
import os.path


def get_transaction(path_to_json):
    if os.path.getsize(path_to_json) == 0:
        return []
    if not os.path.isfile(path_to_json):
        return []

    try:
        with open(path_to_json, encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                return []
    except (json.JSONDecodeError, ValueError):
        print("Ошибка чтения json файла или неверный формат данных")
        return []
