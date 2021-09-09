import calendar
import datetime
import functools
import time
from typing import Any, Callable, Iterator, List, Sequence, TypeVar, Union
from typing import cast

from progress.bar import IncrementalBar

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


F = TypeVar("F", bound=Callable[..., Any])


def show_progress(func: F) -> F:
    """Makes progress bar."""

    @functools.wraps(func)
    def wrapper(arg: Any) -> None:
        func(arg)
        with IncrementalBar("Downloading", suffix="%(percent)d%%") as bar:
            for _ in range(100):
                time.sleep(0.01)
                bar.next()  # noqa: B305
        print("The file has been downloaded to 'Downloads' folder")

    return cast(F, wrapper)
