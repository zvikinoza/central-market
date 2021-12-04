import random
from abc import ABC
from typing import Protocol

from src import constants


class Product(ABC):
    def name(self) -> str:
        pass

    def price(self) -> float:
        pass

    def __str__(self) -> str:
        return f'{self.name()} - {"{:.2f}".format(self.price())}'

    def __repr__(self):
        return str(self)


class Item(Product):
    __name: str
    __price: float

    def __init__(self, name: str, price: float):
        self.__name = name
        self.__price = price

    def price(self) -> float:
        return self.__price

    def name(self) -> str:
        return self.__name


class Pack(Product):
    __name: str
    __price: float
    __products: list[Product]
    __discount_pct: float

    def __init__(self, products: list[Product], discount_pct: float):
        self.__products = products
        self.__discount_pct = discount_pct
        self.__name = ' & '.join(product.name() for product in self.__products)
        self.__price = self.__discount_pct * sum(product.price() for product in self.__products)

    def price(self) -> float:
        return self.__price

    def name(self) -> str:
        return self.__name


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
    def __is_pack(probability: float = constants.PRODUCT_IS_PACK_PROBABILITY) -> bool:
        return random.random() < probability

    @staticmethod
    def __random_name() -> str:
        return random.choice(['Coffee', 'Tea', 'Milk', 'Juice'])

    @staticmethod
    def __random_price() -> float:
        return random.uniform(0.5, 50)
