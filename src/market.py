import random
from typing import Protocol

from src.cashier import Cashier, RandomFreeCashier
from src.manager import ConsoleAskManager
from src.product import Product, RandomProductCreator


class Market(Protocol):
    def get_product_list(self) -> list[Product]:
        pass

    def get_free_cashier(self) -> Cashier:
        pass


class CentralMarket(Market):
    def __init__(self, cashiers: list[Cashier], products: list[Product]):
        self._cashiers = cashiers
        self._products = products

    def get_product_list(self) -> list[Product]:
        return self._products

    def get_free_cashier(self) -> Cashier:
        for cashier in self._cashiers:
            if cashier.is_free():
                return cashier


class MarketCreator(Protocol):
    def create_market(self) -> Market:
        pass


class RandomMarketCreator(MarketCreator):
    def create_market(self) -> Market:
        n_cashiers = random.randrange(1, 5)
        n_products = random.randrange(1, 10)
        manager = ConsoleAskManager()
        cashiers = [RandomFreeCashier(manager) for _ in range(n_cashiers)]
        for cashier in cashiers:
            manager.register_cashier(cashier)
        product_creator = RandomProductCreator()
        products = [product_creator.create_product() for _ in range(n_products)]
        return CentralMarket(cashiers, products)
