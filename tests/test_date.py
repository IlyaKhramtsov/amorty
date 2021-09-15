"""LoanDate representation tests."""

import datetime

import pytest

from amorty.date import LoanDate
from amorty.utils import convert_date

common_dates = [
    datetime.date(2021, 8, 16),
    datetime.date(2021, 9, 15),
    datetime.date(2021, 10, 15),
    datetime.date(2021, 11, 15),
    datetime.date(2021, 12, 15),
]

leap_dates_before_common = [
    datetime.date(2020, 10, 15),
    datetime.date(2020, 11, 16),
    datetime.date(2020, 12, 15),
    datetime.date(2021, 1, 15),
    datetime.date(2021, 2, 15),
]

common_dates_before_leap = [
    datetime.date(2019, 10, 15),
    datetime.date(2019, 11, 15),
    datetime.date(2019, 12, 16),
    datetime.date(2020, 1, 15),
    datetime.date(2020, 2, 17),
]

common_days = [
    datetime.timedelta(days=32),
    datetime.timedelta(days=30),
    datetime.timedelta(days=30),
]

leap_days_before_common = [
    datetime.timedelta(days=30),
    datetime.timedelta(days=32),
    datetime.timedelta(days=29),
    [datetime.timedelta(days=14), datetime.timedelta(days=17)],
    datetime.timedelta(days=31),
]

common_days_before_leap = [
    datetime.timedelta(days=30),
    datetime.timedelta(days=31),
    datetime.timedelta(days=31),
    [datetime.timedelta(days=16), datetime.timedelta(days=14)],
    datetime.timedelta(days=33),
]


def test_wrong_date_format():
    """Check that LoanDate raises an error on invalid date property."""
    with pytest.raises(ValueError):
        LoanDate(5, 5)


def test_string_date():
    """Check that LoanDate is converting a date string to datetime format."""
    assert LoanDate(5, "2021-07-24").date == datetime.date(2021, 7, 24)


def test_datetime_date():
    """Check that LoanDate doesn't change the format 
    when passing a datetime-formatted property.
    """
    loan_date = LoanDate(5, datetime.date(2021, 7, 24))
    assert loan_date.date == datetime.date(2021, 7, 24)


def test_set_working_date():
    """Check that set_working_date returns the next business day."""
    date = datetime.date(2021, 7, 31)
    loan_date = LoanDate(5, date)
    assert loan_date._set_working_date(date) == datetime.date(2021, 8, 2)


@pytest.mark.parametrize(
    "period, date, expected",
    [
        (5, datetime.date(2021, 7, 15), common_dates),
        (5, datetime.date(2020, 9, 15), leap_dates_before_common),
        (5, datetime.date(2019, 9, 15), common_dates_before_leap),
    ],
)
def test_get_working_dates(period, date, expected):
    """Check that get_working_dates returns correct dates.
    In a common year, dates in a transition period from a common year to
    leap year and from leap year to a common year.
    """
    loan_date = LoanDate(period, date)
    assert loan_date.get_working_dates() == expected


@pytest.mark.parametrize(
    "period, date, expected",
    [
        (3, "2021-07-15", common_days),
        (5, datetime.date(2020, 9, 15), leap_days_before_common),
        (5, "2019-09-15", common_days_before_leap),
    ],
)
def test_get_count_days(period, date, expected):
    """Check that get_count_days returns the correct number of days.
    In a common year, days during the transition from a common year to 
    a leap year and from a leap year to a common year.
    """
    loan_date = LoanDate(period, date)
    assert loan_date.get_count_days() == expected
