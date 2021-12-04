import random
from typing import Protocol

from src import constants
from src.manager import Manager
from src.payment import PaymentMethod
from src.product import Product
from src.receipt import Receipt


class Cashier(Protocol):
    def open_receipt(self, products: list[Product]) -> Receipt:
        pass

    def process_payment(self, receipt: Receipt, payment_method: PaymentMethod) -> bool:
        """
        :returns: True if payment was successful, False otherwise
        :rtype: bool
        """
        pass

    def __close_receipt(self, receipt: Receipt):
        pass

    def is_free(self) -> bool:
        pass

    def clean_up_and_end_shift(self) -> None:
        pass

    def get_report(self) -> (list[Receipt], float):
        pass


class BasicCashier(Cashier):
    __takings: float
    __manager: Manager
    __free_cashier_probability: float
    __closed_receipts: list[Receipt]

    def __init__(self, manager: Manager):
        self.__manager = manager
        self.__closed_receipts = []
        self.__takings = 0.0
        self.__n_closed_receipts = 0

    def open_receipt(self, products: list[Product]) -> Receipt:
        return Receipt(products)

    def process_payment(self, receipt: Receipt, payment_method: PaymentMethod) -> bool:
        """
        :returns: True if payment was successful, False otherwise
        :rtype: bool
        """
        total_price = receipt.total_price()
        if payment_method.pay(total_price) == total_price:
            self.__takings += total_price
            self.__close_receipt(receipt)
            return True
        return False

    def __close_receipt(self, receipt: Receipt):
        self.__closed_receipts.append(receipt)
        self.__n_closed_receipts += 1
        if self.__n_closed_receipts == constants.SHIFT_END_THRESHOLD and self.__manager.should_send_report():
            pass
        elif self.__n_closed_receipts == constants.REPORT_THRESHOLD and self.__manager.should_end_shift():
            self.__closed_receipts = []

    def is_free(self) -> bool:
        return True

    def clean_up_and_end_shift(self) -> None:
        self.__closed_receipts = []
        self.__takings = 0.0

    def get_report(self) -> (list[Receipt], float):
        return list(self.__closed_receipts), self.__takings


class RandomFreeCashier(BasicCashier):
    __free_cashier_probability: float

    def __init__(self, manager: Manager, free_cashier_probability: float = constants.FREE_CASHIER_PROBABILITY):
        super().__init__(manager)
        self.__free_cashier_probability = free_cashier_probability

    def is_free(self) -> bool:
        """
        :returns: True with probability of self.__free_cashier_probability, False otherwise
        """
        return random.random() < self.__free_cashier_probability
