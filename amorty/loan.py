import datetime
from abc import ABC, abstractmethod
from collections import namedtuple
from typing import Union, List, Iterator

from amorty.date import LoanDate
from amorty import utils


LoanDetails = namedtuple("LoanDetails", "date day principal interest payment balance")


class Loan(ABC):
    """Abstract class for building different kinds of loans"""

    def __init__(
        self,
        amount: Union[int, float],
        period: int,
        rate: Union[int, float],
        date: Union[datetime.date, str],
    ):
        """Construct a new loan.

        Args:
            amount: loan amount
            period: loan term in months
            rate: annual percentage rate
            date: date of issue of the loan
        """
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
            raise ValueError(
                "Interest rate must be int or float type and positive number"
            )

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

    def _calculate_accrued_interest(
        self,
        balance_reminder: Union[float, int],
        day: Union[datetime.timedelta, List[datetime.timedelta]],
        date: datetime.date,
    ) -> float:
        """Calculates accrued interest in the current period.

        Args:
            balance_reminder: balance in the current period
            day: number of days in the current period
            date: payment date
        Returns:
            float
        """
        interest_rate = self._rate / 100
        days_to_year_ratio = utils.convert_days_to_year(day, date)
        return balance_reminder * interest_rate * days_to_year_ratio

    def create_loan(self) -> Iterator:
        loan_amortization = self.amortize()
        dates = self.date.get_working_dates()
        days = utils.clear_days(self.date.get_count_days())

        for date, day, (payment, balance, principal, interest) in zip(
            dates, days, loan_amortization
        ):
            loan_details = LoanDetails(date, day, principal, interest, payment, balance)
            yield loan_details


class Annuity(Loan):
    """Annuity loan type.

    Implements the calculation of payments for the annuity scheme of repayment.
    """

    def _calculate_monthly_interest(self) -> float:
        """Calculates monthly interest rate"""
        return self._rate / 1200

    def _get_annuity_coefficient(self) -> float:
        monthly_rate = self._calculate_monthly_interest()
        numerator = monthly_rate * (1 + monthly_rate) ** self._period
        denominator = (1 + monthly_rate) ** self._period - 1
        return numerator / denominator

    def get_annuity_payment(self):
        return self._amount * self._get_annuity_coefficient()

    def _calculate_principal(self, accrued_interest: float) -> float:
        return self.get_annuity_payment() - accrued_interest

    def amortize(self):
        """Calculates amortization for an annuity repayment scheme."""
        balance_reminder = self._amount
        period = self._period
        date = (x for x in self.date.get_working_dates())
        day = (x for x in self.date.get_count_days())

        while period:
            accrued_interest = self._calculate_accrued_interest(
                balance_reminder, next(day), next(date)
            )
            principal = self._calculate_principal(accrued_interest)
            balance_reminder -= principal
            if period <= 1:
                principal += balance_reminder
                balance_reminder -= balance_reminder
            payment = accrued_interest + principal
            yield payment, balance_reminder, principal, accrued_interest
            period -= 1


class StraightLine(Loan):
    """Straight-line loan type.

    Implements the calculation of payments for the differentiated scheme of repayment.
    The differentiated payment method implies that:
        - the principal amount is distributed over the period of payment in the equal
          installments;
        - the loan interest accrued on the balance.

    Methods
    --------
    amortize(): Calculates amortization for a differentiated repayment scheme
    """

    def _calculate_principal(self) -> float:
        return self._amount / self._period

    def amortize(self):
        """Calculates amortization for a differentiated repayment scheme."""
        balance_reminder = self._amount
        period = self._period
        date = (x for x in self.date.get_working_dates())
        day = (x for x in self.date.get_count_days())

        while period:
            accrued_interest = self._calculate_accrued_interest(
                balance_reminder, next(day), next(date)
            )
            principal = self._calculate_principal()
            payment = principal + accrued_interest
            balance_reminder -= principal
            yield payment, balance_reminder, principal, accrued_interest
            period -= 1
