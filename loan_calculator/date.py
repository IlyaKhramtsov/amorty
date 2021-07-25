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

