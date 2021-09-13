"""Module for loan.py, providing some additional facilities."""

import calendar
import datetime
from typing import Union, List

import holidays

from amorty import utils


class LoanDate:
    """LoanDate implements the dates of the loan payments.

    Attributes
    ----------
    period: int, required
        Loan term (specified in months)
    date : str, datetime.date, required
        Date of issue of the loan

    Methods
    -------
    get_working_dates()
        Calculates the dates on which the monthly payments on the loan will be paid
    get_count_days()
        Calculates the number of days between monthly loan payments
    """

    def __init__(self, period: int, date: Union[str, datetime.date]) -> None:
        self.period = period
        self.date = date

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date: Union[str, datetime.date]) -> None:
        if isinstance(date, (str, datetime.date)):
            self._date = utils.convert_date(date)
        else:
            raise ValueError("Date must be string type or datetime.date type")

    def get_working_dates(self) -> List[datetime.date]:
        """Creates a list of dates excluding weekends."""
        dates = []
        current_date = self._date
        period = self.period

        while period:
            days_in_current_month = calendar.monthrange(
                current_date.year, current_date.month
            )[1]
            current_date += datetime.timedelta(days=days_in_current_month)
            dates.append(self._set_working_date(current_date))
            period -= 1
        return dates

    @staticmethod
    def _set_working_date(date: datetime.date) -> datetime.date:
        """Checks and return a date after a day off.

        If the payment date is a weekend of holiday, the date is transferred
        to the next business day.
        """
        while date.weekday() in holidays.WEEKEND or date in holidays.RUS():
            date += datetime.timedelta(days=1)
        return date

    def get_count_days(
        self,
    ) -> List[Union[datetime.timedelta, List[datetime.timedelta]]]:
        """Calculates the difference between dates in a list."""
        days: List[Union[datetime.timedelta, List[datetime.timedelta]]] = []
        dates = self.get_working_dates()
        start_date = self._date
        days.append(dates[0] - start_date)

        for date, next_date in zip(dates, dates[1:]):
            start_year = datetime.date(next_date.year, 1, 1)

            if date.month == 12 and calendar.isleap(next_date.year):
                common_date, leap_date = start_year - date, next_date - start_year
                days.append([common_date, leap_date])

            elif date.month == 12 and calendar.isleap(date.year):
                leap_date, common_date = start_year - date, next_date - start_year
                days.append([common_date, leap_date])

            else:
                days.append(next_date - date)
        return days
