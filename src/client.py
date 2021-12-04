import random
from typing import Protocol

from src.payment import PaymentMethod, CashPaymentMethod, CreditCardPaymentMethod
from src.product import Product


class Client(Protocol):
    def choose_products(self, products: list[Product]) -> list[Product]:
        pass

    def get_payment_method(self) -> PaymentMethod:
        pass


class RandomClient(Client):
    def choose_products(self, products: list[Product]) -> list[Product]:
        return random.sample(products, random.randint(1, len(products)))

    def get_payment_method(self) -> PaymentMethod:
        return random.choice([CashPaymentMethod(), CreditCardPaymentMethod()])
