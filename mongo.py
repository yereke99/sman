from pymongo import MongoClient

class MongoDB:
    def __init__(self, host='localhost', port=27017, db_name='shoe_database'):
        """Инициализация подключения к MongoDB без аутентификации."""
        connection_string = f"mongodb://{host}:{port}/{db_name}"
        self.client = MongoClient(connection_string)
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

    def get_price_by_code(self, code: str):
        """Извлекает текущую цену по коду товара."""
        result = self.collection.find_one({"code": code}, {"discounted_price": 1})
        return result["discounted_price"] if result else None

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
        
    def upsert_item(self, code, item_data):
        """Добавляет или обновляет данные по коду товара."""
        result = self.collection.update_one(
            {"code": code},  # Поиск по коду
            {"$set": item_data},  # Обновление данных
            upsert=True  # Если не найдено, создаем новый документ
        )
        return result.upserted_id if result.upserted_id else "Updated"

    def display_all_items(self):
        """Отображает все элементы в коллекции."""
        items = list(self.collection.find())
        for item in items:
            print(item)

if __name__ == "__main__":
    db = MongoDB()
    db.display_all_items()
