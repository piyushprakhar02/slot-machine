from datetime import datetime


def is_today(date):
    """Check if the provided date is today's date"""
    return date.date() == datetime.today().date()
