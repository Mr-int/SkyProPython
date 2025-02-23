from typing import Any


def filter_by_state(list_of_dicts: list[Any], state: str = "EXECUTED") -> list[Any]:
    """Проверяет значение в словарях на заданное и если оно совпадает то, выводит его"""
    correct_list = []
    for i in range(0, len(list_of_dicts) - 1):
        if list_of_dicts[i]["state"] == state:
            correct_list.append(list_of_dicts[i])

    return correct_list


def sort_by_date(list_of_dicts: list[Any], sort_order: bool = True) -> list[Any]:
    """Сортирует список по датам в словарях по убывание(по умолчанию)"""
    correct_list_of_data = []
    correct_list_of_data = sorted(
        list_of_dicts, key=lambda x: x.get("date"), reverse=sort_order
    )

    return correct_list_of_data
