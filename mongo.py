from pymongo import MongoClient

class MongoDB:
    def __init__(self, host='localhost', port=27017, db_name='shoe_database'):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db['shoes']

    def insert_item(self, item_data):
        """Вставляет данные в коллекцию MongoDB."""
        result = self.collection.insert_one(item_data)
        return result.inserted_id

    def get_all_items(self):
        """Извлекает все записи из коллекции."""
        return list(self.collection.find())

    def getBySexPrice(self, sex: str, price: str):
        """Извлекает записи по категории (полу) и цене со скидкой."""
        query = {"category": sex, "discounted_price": price}
        return list(self.collection.find(query))

    def getByCodeSize(self, code: str) -> [int]:
        """Извлекает размеры по коду товара."""
        result = self.collection.find_one({"code": code}, {"sizes": 1})
        return result["sizes"] if result else []

    def getByCodeAllData(self, code: str):
        """Извлекает все данные по коду товара."""
        return self.collection.find_one({"code": code})

    # Метод класса MongoDB для получения текущей цены по коду товара
    def get_price_by_code(self, code: str):
        """Извлекает текущую цену по коду товара."""
        result = self.collection.find_one({"code": code}, {"discounted_price": 1})
        return result["discounted_price"] if result else None

    # Метод класса MongoDB для получения цены по коду и размеру
    def get_price_by_code_and_size(self, code: str, size: int):
        """Извлекает текущую цену по коду товара и размеру."""
        result = self.collection.find_one({"code": code, "sizes": size}, {"discounted_price": 1})
        return result["discounted_price"] if result else None
    
    def remove_item_from_inventory(self, code: str, size: int):
        """Удаляет указанный размер из списка размеров по коду товара."""
        # Находим документ с указанным кодом и удаляем размер
        result = self.collection.update_one(
            {"code": code},
            {"$pull": {"sizes": size}}
        )
        # Возвращаем True, если один документ был обновлен, иначе False
        return result.modified_count > 0
    # Метод для отображения всех элементов в коллекции
    def display_all_items(self):
        items = list(self.collection.find())
        for item in items:
            print(item)

if __name__ == "__main__":
    db = MongoDB()
    db.display_all_items()