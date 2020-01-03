"""
Date utility functions.
"""


def is_leap_year(year):
    """
    Return true if year is a leap year.
    Year is leap year if it's a multiple of 4 and
        (it's not a multiple of 100 or it's a multiple of 400)
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
