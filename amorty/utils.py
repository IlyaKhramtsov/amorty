import calendar
import datetime
from typing import Iterator, List, Sequence, Union


DAYS_IN_YEAR = {
    "common year": 365,
    "leap year": 366,
}


def convert_date(date: Union[str, datetime.date]) -> datetime.date:
    """Convert string to datetime.date object."""
    if isinstance(date, str):
        return datetime.date.fromisoformat(date)
    return date


def convert_days_to_year(
    day: Union[datetime.timedelta, List[datetime.timedelta]], date: datetime.date
) -> float:
    """Calculate the ratio of days to year depending on its type."""
    if isinstance(day, list):
        return (day[0].days / DAYS_IN_YEAR["common year"]) + (
            day[1].days / DAYS_IN_YEAR["leap year"]
        )
    return day.days / set_year_type(date)


def set_year_type(date: datetime.date) -> int:
    """Checks the number of days in a year for a specific date."""
    if calendar.isleap(date.year):
        return DAYS_IN_YEAR["leap year"]
    return DAYS_IN_YEAR["common year"]


def clear_days(
    days: Sequence[Union[datetime.timedelta, List[datetime.timedelta]]]
) -> Iterator[int]:
    """Search for a nested list of days and add those values."""
    for day in days:
        if isinstance(day, list):
            yield (day[0] + day[1]).days
        else:
            yield day.days
