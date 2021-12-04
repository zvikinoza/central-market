from typing import Protocol


class PaymentMethod(Protocol):
    def pay(self, amount):
        pass


class CashPaymentMethod(PaymentMethod):
    def pay(self, amount):
        print(f'Paying {amount} with cash')


class CreditCardPaymentMethod(PaymentMethod):
    def pay(self, amount):
        print(f'Paying {amount} with card')
