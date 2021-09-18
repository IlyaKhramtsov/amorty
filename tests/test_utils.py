import datetime

import pytest

from amorty.utils import convert_date, set_year_type


@pytest.mark.parametrize("date", [(datetime.date(2021, 9, 13)), ("2021-09-13")])
def test_convert_date(date):
    expected = datetime.date(2021, 9, 13)
    assert convert_date(date) == expected


@pytest.mark.parametrize(
    "date, expected",
    [(datetime.date(2019, 5, 23), 365), (datetime.date(2020, 7, 18), 366)],
)
def test_year_type(date, expected):
    assert set_year_type(date) == expected
