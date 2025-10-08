import json
import os
from dataclasses import dataclass

from app.source.schemas import SProduct


# Получаем путь к JSON
path_to_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'products.json')

# Для сохранения в файл (если понадобится)
def dict_list_to_json(dict_list, filename):
    """
    Преобразует список словарей в JSON-строку и сохраняет её в файл.

    :param dict_list: Список словарей
    :param filename: Имя файла для сохранения JSON-строки
    :return: JSON-строка или None в случае ошибки
    """
    try:
        json_str = json.dumps(dict_list, ensure_ascii=False)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(json_str)
        return json_str
    except (TypeError, ValueError, IOError) as e:
        print(f"Ошибка при преобразовании списка словарей в JSON или записи в файл: {e}")
        return None


def json_to_dict_list(filename):
    """
    Преобразует JSON-строку из файла в список словарей.

    :param filename: Имя файла с JSON-строкой
    :return: Список словарей или None в случае ошибки
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            json_str = file.read()
            # dict_list = json.dumps(json_str)
            dict_list = json.loads(json_str)
        return dict_list
    except (TypeError, ValueError, IOError) as e:
        print(f"Ошибка при чтении JSON из файла или преобразовании в список словарей: {e}")
        return None

@dataclass
class ProductsDao:
    products = json_to_dict_list(path_to_json)

    @classmethod
    async def find_all(cls):
        return cls.products

    @classmethod
    async def update(cls, product_id: int, product: SProduct):
        search_id = None
        for index, product_c in enumerate(cls.products):
            product_c_id = product_c.get("id")
            if product_c_id == str(product_id):
                search_id = index
                for key, value in product.__dict__.items():
                    cls.products[index][key] = value
                break
        return search_id

    @classmethod
    async def delete(cls, product_id: int):
        search_id = None
        for index, product_c in enumerate(cls.products):
            product_c_id = product_c.get("id")
            if product_c_id == str(product_id):
                search_id = index
                del cls.products[index]
                break
        return search_id
