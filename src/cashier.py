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

    def __prompt_manager_for_report(self) -> bool:
        pass

    def __prompt_manager_to_end_shift(self) -> bool:
        pass

    def is_free(self) -> bool:
        pass

    def clean_up_and_end_shift(self):
        pass


class RandomFreeCashier(Cashier):
    __takings: int
    __manager: Manager
    __free_cashier_probability: float
    __closed_receipts: list[Receipt]

    def __init__(self, manager: Manager, free_cashier_probability: float = 0.6):
        self.__manager = manager
        self.__free_cashier_probability = free_cashier_probability
        self.__closed_receipts = []
        self.__takings = 0

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
        n_closed_receipts = len(self.__closed_receipts)
        if n_closed_receipts == constants.SHIFT_END_THRESHOLD and self.__prompt_manager_to_end_shift():
            pass
        if n_closed_receipts >= constants.REPORT_THRESHOLD and self.__prompt_manager_for_report():
            self.__closed_receipts = []

    def __prompt_manager_for_report(self) -> bool:
        return self.__manager.should_send_report()

    def __prompt_manager_to_end_shift(self) -> bool:
        return self.__manager.should_end_shift()

    def is_free(self) -> bool:
        return random.random() < self.__free_cashier_probability

    def clean_up_and_end_shift(self):
        self.__closed_receipts = []
        self.__takings = 0
