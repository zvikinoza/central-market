from typing import Protocol

from src import constants


class Manager(Protocol):
    def should_send_report(self) -> bool:
        pass

    def should_end_shift(self) -> bool:
        pass

    def register_cashier(self, cashier) -> None:
        pass


class ConsoleAskManager(Manager):
    def __init__(self):
        self.__cashiers = []
        self.__n_shift = 0

    def should_send_report(self) -> bool:
        print('Do you want to see the report?')
        return input('(y/n) ') == 'y'

    def should_end_shift(self) -> bool:
        print('Do you want to end the shift?')
        end = input('(y/n) ') == 'y'
        if end:
            self.__n_shift += 1
        if self.__n_shift >= constants.SHIFTS_PER_DAY:
            print('You have ended the shift {} times. You should end the day.'.format(self.__n_shift))
            exit(0)
        return end

    def register_cashier(self, cashier) -> None:
        self.__cashiers.append(cashier)
