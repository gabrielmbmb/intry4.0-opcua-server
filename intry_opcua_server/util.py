import datetime


def str_to_date(str_date) -> datetime.datetime:
    """Parses a date in string format to date type.

    Args:
        str_date (str): the date in string format.

    Returns:
        datetime.datetime: parsed date.
    """
    return datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")
