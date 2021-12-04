import random
from typing import Protocol


class Product(Protocol):
    def price(self) -> float:
        pass


class ProductCreator(Protocol):
    def create_product(self) -> Product:
        pass


class RandomProductCreator(ProductCreator):
    def create_product(self) -> Product:
        if self.__is_pack():
            n_products, discount_pct = self.__random_pack_info()
            return Pack([self.create_product() for _ in range(n_products)], discount_pct)
        return Item(self.__random_name(), self.__random_price())

    @staticmethod
    def __random_pack_info() -> (int, float):
        n_products = random.randint(1, 5)
        discount_pct = random.uniform(0, 0.5)
        return n_products, discount_pct

    @staticmethod
    def __is_pack(probability: float = 0.3) -> bool:
        return random.random() < probability

    @staticmethod
    def __random_name() -> str:
        return random.choice(['Coffee', 'Tea', 'Milk', 'Juice'])

    @staticmethod
    def __random_price() -> float:
        return random.uniform(0.5, 50)


class Item(Product):
    def __init__(self, name: str, price: float):
        self.__name = name
        self.__price = price

    def price(self) -> float:
        return self.__price

    def name(self) -> str:
        return self.__name


class Pack(Product):
    products: list[Product]

    def __init__(self, products: list[Product], discount_pct: float):
        self.__products = products
        self.__discount_pct = discount_pct

    def price(self) -> float:
        total_price = sum(product.price() for product in self.__products)
        return self.__discount_pct * total_price
