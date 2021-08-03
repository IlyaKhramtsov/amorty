import calendar
import datetime

from typing import Union, List

from loan_calculator import utils


class LoanDate:

    def __init__(self, period: int, date: Union[str, datetime.date]) -> None:
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
            raise ValueError('Date must be string type or datetime.date type')

    def get_working_dates(self):
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

    def get_count_days(self) -> List[Union[datetime.timedelta, list[datetime.timedelta]]]:
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


