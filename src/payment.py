from typing import Protocol


class PaymentMethod(Protocol):
    def pay(self, amount) -> float:
        pass


class CashPaymentMethod(PaymentMethod):
    def pay(self, amount) -> float:
        # print(f'Paying {"{:.2f}".format(amount)} with cash')
        return amount


class CreditCardPaymentMethod(PaymentMethod):
    def pay(self, amount) -> float:
        # print(f'Paying {"{:.2f}".format(amount)} with card')
        return amount
