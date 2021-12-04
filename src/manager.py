from typing import Protocol

from src import constants


class Manager(Protocol):
    def should_send_report(self) -> bool:
        pass

    def should_end_shift(self) -> bool:
        pass

    def register_cashier(self, cashier) -> None:
        pass

    def __send_report(self) -> None:
        pass


class ConsoleAskManager(Manager):
    def __init__(self):
        self.__cashiers = []
        self.__n_shift = 0

    def should_send_report(self) -> bool:
        print('Do you want to see the report?')
        end = input('(y/n) ') == 'y'
        if end:
            self.__send_report()
        return end

    def should_end_shift(self) -> bool:
        print('Do you want to end the shift?')
        end = input('(y/n) ') == 'y'
        if end:
            self.__n_shift += 1
            self.__send_report()
        if self.__n_shift >= constants.SHIFTS_PER_DAY:
            print('You have ended the shift {} times. You should end the day.'.format(self.__n_shift))
            exit(0)
        return end

    def register_cashier(self, cashier) -> None:
        self.__cashiers.append(cashier)

    def __send_report(self):
        total_takings = 0.0
        for cashier in self.__cashiers:
            receipts, takings = cashier.get_report()
            total_takings += takings
            print(receipts)
        print(f'Total Revenue: {"{:.2f}".format(total_takings)}')
