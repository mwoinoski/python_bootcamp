"""
Date normalization functions.
"""

import re

days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


# TODO: add the simplest possible code that will make the first test case pass

def normalize_date(date):
    """
    Converts a date to ISO 8601 format (YYYY-MM-DD)

    Valid values for input_date_fmt:
        YMD - YYYY-MM-DD
        DMY - DD-MM-YYYY
        MDY - MM-DD-YYYY
    """
    return None
    # HINT: remember the Python syntax for substring operations:
    #       input[0]    char 0 (the first character)
    #       input[0:4]  chars 0 through 3 (that is, 0 up to but not including 4)
    #       input[6:]   chars 6 through the end of the string
    #       input[:4]   chars 0 through 3
    #       input[-1]   last char


def is_leap_year(year):
    """
    Return true if year is a leap year.
    Year is leap year if it's a multiple of 4 and
        (it's not a multiple of 100 or it's a multiple of 400)
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
