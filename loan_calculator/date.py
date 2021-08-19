"""Module for loan.py, providing some additional facilities"""

import calendar
import datetime

from typing import Union

from loan_calculator import utils


class LoanDate:
    """LoanDate implements the dates of the loan payments.

    Attributes
    ----------
    period: int, requared
        Loan term (specified in mounths)
    date : str, datetime.date, requared
        Date of issue of the loan

    Methods
    -------
    get_working_dates()
        Calculates the dates on which the monthly payments on the loan will be paid
    get_count_days()
        Calculates the number of days between monthly loan payments
    """

    def __init__(self, period: int, date: Union[str, datetime.date]) -> None:
        """Initialize loan date"""
        self.period = period
        self.date = date

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date: Union[str, datetime.date]):
        if isinstance(date, (str, datetime.date)):
            self._date = utils.convert_date(date)
        else:
            raise ValueError("Date must be string type or datetime.date type")

    def get_working_dates(self) -> list[datetime.date]:
        """Creates a list of dates excluding weekends."""
        dates = []
        current_date = self._date
        period = self.period

        while period:
            days_in_current_month = calendar.monthrange(
                current_date.year, current_date.month
            )[1]
            current_date += datetime.timedelta(days=days_in_current_month)
            dates.append(utils.check_date(current_date))
            period -= 1
        return dates

    def get_count_days(self) -> list[datetime.timedelta]:
        """Calculates the difference between dates in a list."""
        days = []
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
