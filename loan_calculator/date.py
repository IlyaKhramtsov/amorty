import calendar
import datetime

from typing import Union

from . import utils


class LoanDate:

    def __init__(self, period: int, date: Union[str, datetime.date]) -> None:
        self.period = period
        self.date = date

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value: Union[str, datetime.date]):
        if isinstance(value, (str, datetime.date)):
            self._date = utils.convert_date(value)
        else:
            raise ValueError('Date must be string type or datetime.date type')

    def get_dates(self):
        """Creates a list of dates excluding weekends."""
        dates = []
        current_date = self._date
        period = self.period

        while period:
            days_in_current_month = calendar.monthrange(current_date.year, current_date.month)[1]
            current_date += datetime.timedelta(days=days_in_current_month)
            dates.append(utils.check_date(current_date))
            period -= 1
        return dates



