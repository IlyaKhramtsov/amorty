import datetime
from abc import ABC, abstractmethod
from typing import Union

from loan_calculator.date import LoanDate

class BaseLoan(ABC):
    """Abstract class for building different kinds of loans"""

    def __init__(self, amount: Union[int, float],
                period: int,
                rate: Union[int, float],
                date: Union[datetime.date, str]):
        self.amount = amount
        self.period = period
        self.rate = rate
        self.date = LoanDate(period, date)

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount: Union[int, float]):
        if isinstance(amount, (int, float)) and amount > 0:
            self._amount = amount
        else:
            raise ValueError("Amount must be int or float type and positive number")

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, rate: Union[int, float]):
        if isinstance(rate, (int, float)) and rate > 0:
            self._rate = rate
        else:
            raise ValueError("Interest rate must be int or float type and positive number")

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, period: int):
        if isinstance(period, int) and period > 0:
            self._period = period
        else:
            raise ValueError("Period must be integer type and positive number")

    def __str__(self):
        return f"\namount: {self._amount}\nrate: {self._rate}%\nperiod: {self._period} months"

    @abstractmethod
    def amortize(self):
        pass

