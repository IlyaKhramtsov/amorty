import datetime
import calendar
import holidays
from typing import Union, List


DAYS_IN_YEAR = {
        "common year": 365,
        "leap year": 366,
        }

def convert_date(date):
    """Convert string to datetime.date object"""
    if isinstance(date, str):
        return datetime.date.fromisoformat(date)
    return date

def check_date(date: datetime.date) -> datetime.date:
    """Checks and returns a date after a day off."""
    while date.weekday() in holidays.WEEKEND or date in holidays.RUS():
        date += datetime.timedelta(days=1)
    return date

def set_days_count(day: datetime.timedelta, date: datetime.date) -> float:
    if isinstance(day, list):
        return (day[0].days / DAYS_IN_YEAR["common year"]) + (day[1].days / DAYS_IN_YEAR["leap year"])
    return day.days / check_year_type(date)

def check_year_type(date: datetime.date) -> int:
    if calendar.isleap(date.year):
        return DAYS_iN_YEAR["leap year"]
    return DAYS_IN_YEAR["common year"]

def clear_days(days: List[Union[datetime.timedelta, List[datetime.timedelta]]]):
    for day in days:
        if isinstance(day, list):
            yield (day[0] + day[1]).days
        yield day.days
