import datetime
from abc import ABC, abstractmethod
from typing import Union

from loan_calculator.date import LoanDate
from loan_calculator.utils import set_days_count

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

    def _calculate_accrued_interest(self, balance_reminder: int, day: datetime.timedelta, date: datetime.date) -> float:
        interest_rate = self._rate / 100
        days_count = set_days_count(day, date)
        return balance_reminder * interest_rate * days_count


class AnnuityLoan(BaseLoan):

    def _calculate_monthly_interest(self) -> float:
        """Calculates monthly interest rate"""
        return self._rate / 1200

    def get_annuity_payment(self) -> float:
        monthly_rate = self._calculate_monthly_interest()
        numerator = monthly_rate * (1 + monthly_rate) ** self._period
        denominator = (1 + monthly_rate) ** self._period - 1
        return self._amount * (numerator / denominator)

    def _calculate_principal(self, accrued_interest: float) -> float:
        return self.get_annuity_payment() - accrued_interest

    def amortize(self):
        """The calculation of annuity payments on the loan"""
        balance_reminder = self._amount
        period = self._period
        date = (x for x in self.date.get_working_dates())
        day = (x for x in self.date.get_count_days())

        while period:
            accrued_interest = self._calculate_accrued_interest(balance_reminder, next(day), next(date))
            principal = self._calculate_principal(accrued_interest)
            balance_reminder -= principal
            if period <= 1:
                principal += balance_reminder
                balance_reminder -= balance_reminder
            payment = accrued_interest + principal
            yield payment, balance_reminder, principal, accrued_interest
            period -= 1


class DifferentiatedLoan(BaseLoan):
    """The differentiated payment method implies that:
        the principal amount is distributed over the period of payment in the equal installments;
        the loan interet accrued on the balance."""

    def _calculate_principal(self) -> float:
        return self._amount / self._period

    def amortize(self):
        """The calculation of payments for differentiated scheme of repayment."""
        balance_reminder = self._amount
        period = self._period
        date = (x for x in self.date.get_working_dates())
        day = (x for x in self.date.get_count_days())

        while period:
            accrued_interest = self._calculate_accrued_interest(balance_reminder, next(day), next(date))
            principal = self._calculate_principal()
            payment = principal + accrued_interest
            balance_reminder -= principal
            yield payment, balance_reminder, principal, accrued_interest
            period -= 1
