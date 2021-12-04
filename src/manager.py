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

    def end_shift(self) -> None:
        pass


class BasicManager(Manager):
    def __init__(self):
        self._cashiers = []
        self._n_shift = 0

    def should_send_report(self) -> bool:
        """
        Always Returns True. The should send the report.
        """
        self.__send_report()
        return True

    def should_end_shift(self) -> bool:
        """
        Always Returns True. The manager should end the shift.
        """
        self.end_shift()
        return True

    def end_shift(self) -> None:
        self._n_shift += 1
        self.__send_report()
        if self._n_shift >= constants.SHIFTS_PER_DAY:
            exit(0)

    def register_cashier(self, cashier) -> None:
        self._cashiers.append(cashier)

    def __send_report(self) -> None:
        pass


class ConsoleAskManager(BasicManager):
    """
    Manager that asks the user if he wants to send the report or end the shift.
    Pretty Nice Guy
    """
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
            super().end_shift()
        return end

    def __send_report(self):
        total_takings = 0.0
        for cashier in self._cashiers:
            receipts, takings = cashier.get_report()
            total_takings += takings
            print(*receipts, sep='\n')
        print(f'Total Revenue: {"{:.2f}".format(total_takings)}')
