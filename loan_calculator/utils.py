import datetime
import holidays


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
