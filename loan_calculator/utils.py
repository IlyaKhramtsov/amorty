import datetime


def convert_date(date):
    """Convert string to datetime.date object"""
    if isinstance(date, str):
        return datetime.date.fromisoformat(date)
    return date
