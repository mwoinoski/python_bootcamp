"""
Date normalization functions.
"""

import re

days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def normalize_date(date, input_date_fmt='YMD'):
    """ Converts a date to ISO 8601 format (YYYY-MM-DD) """
    if input_date_fmt == 'YMD':
        year = date[0:4]
        month = int(date[5:7])
        day = int(date[8:])
    elif input_date_fmt == 'DMY':
        year = get_four_digit_year(date[6:])
        month = int(date[3:5])
        day = int(date[0:2])
    elif input_date_fmt == 'MDY':
        year = get_four_digit_year(date[6:])
        month = int(date[0:2])
        day = int(date[3:5])
    else:
        print(f'Date format "{input_date_fmt}" not recognized')
        return None

    if month < 1 or month > 12:
        print(f'Date {date} has invalid month {month} for format '
              f'{input_date_fmt}')
        return None

    max_day = days_in_month[month - 1]
    if month == 2 and is_leap_year(year):
        max_day += 1
    if day < 1 or day > max_day:
        print(f'Date {date} has invalid day {day} for format {input_date_fmt}')
        return None

    normalized_date = f'{year}-{month:02d}-{day:02d}'

    return normalized_date


def get_four_digit_year(year):
    """ Converts two-digit years to four-digit years """
    year = int(year)
    if year < 100:
        year += 2000
    return year


def is_leap_year(year):
    """
    Return true if year is a leap year.
    Year is leap year if it's a multiple of 4 and
        (it's not a multiple of 100 or it's a multiple of 400)
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
