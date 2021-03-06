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
        return f'name={self.name()} - price={"{:.2f}".format(self.price())}'

    def __repr__(self):
        return str(self)


class Item(Product):
    __name: str
    __price: float
    """ 
    To have discount on single item please use Pack of Items with just one item.
    """
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
    """
    Name and price are calculated according to the products in the pack.
    Note: if two packs have discount and one is in other, both discount will be applied. 
    """
    def __init__(self, products: list[Product], discount_pct: float):
        self.__products = products
        self.__discount_pct = discount_pct
        self.__name = ' & '.join(product.name() for product in self.__products)
        self.__price = (1.0 - self.__discount_pct) * sum(product.price() for product in self.__products)

    def price(self) -> float:
        return self.__price

    def name(self) -> str:
        return self.__name


class ProductCreator(Protocol):
    def create_product(self) -> Product:
        pass


class RandomProductCreator(ProductCreator):
    def create_product(self, n_nested_packs: int = 0) -> Product:
        if n_nested_packs < constants.NESTED_PACKS_LIMIT and self.__is_pack():
            n_products, discount_pct = self.__random_pack_info()
            return Pack([self.create_product(n_nested_packs+1) for _ in range(n_products)], discount_pct)
        return Item(self.__random_name(), self.__random_price())

    @staticmethod
    def __random_pack_info() -> (int, float):
        n_products = random.randint(1, 5)
        discount_pct = random.uniform(0, 0.5)
        return n_products, discount_pct

    @staticmethod
    def __is_pack() -> bool:
        return random.random() < constants.PRODUCT_IS_PACK_PROBABILITY

    @staticmethod
    def __random_name() -> str:
        return random.choice(constants.PRODUCT_NAMES)

    @staticmethod
    def __random_price() -> float:
        return random.uniform(0.5, 50)
