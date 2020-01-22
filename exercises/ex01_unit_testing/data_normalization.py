"""
Date utility functions.
"""

from collections import Counter
from datetime import datetime
from enum import Enum, unique
import re
from typing import List, Dict


# TODO: this is the first function you'll test (no code changes required here)

def is_leap_year(year):
    """
    Return true if year is a leap year.
    Year is leap year if it's a multiple of 4 and
        (it's not a multiple of 100 or it's a multiple of 400)
    """
    # return true
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def normalize_column_name(name, max_len=64):
    """
    Return a normalized version of the column name.
    Requirements for normalized column name:
        A name that is None or an empty string is normalized to an empty string
        Otherwise, the name consists only of lower case letters, numbers, and '_'
        All other characters are converted to '_'
        Multiple consecutive occurences of '_' will be replaced by a single '_'
        Leading and trailing '_' will be deleted
        Name will be shortened to max_len characters
    """
    new_name = ''
    if name:
        new_name = name
        new_name = re.sub(r'\W', '_', new_name)  # convert special chars to '_'
        new_name = re.sub(r'_+', '_', new_name)  # replace multiple '_' with one
        new_name = new_name.lower()
        new_name = new_name.lstrip('_')  # remove leading '_'
        new_name = new_name[:max_len]
        new_name = new_name.rstrip('_')  # remove trailing '_'
    return new_name
    # return re.sub(r'_+', '_', re.sub(r'\W', '_', name)) \
    #          .lower().lstrip('_')[:max_len].rstrip('_') if name else ''


def count_occurrences(cols):
    """
    Return a dictionary of (column-name, number-of-occurences).
    Assumes the names in the argument list have been normalized.
    """
    return dict(Counter(cols))  # Counter is a dictionary-like object


def identify_duplicate_columns(cols, how_many = None):
    """
    Return a dictionary with the name and count of occurrences for each
    duplicate name in the argument `cols`. Names that are not duplicated
    are not present in the returned dictionary.
    """
    if not how_many:
        how_many = count_occurrences(cols)
    how_many_dupes_left = {}
    for col in how_many:
        if how_many[col] > 1:
            how_many_dupes_left[col] = how_many[col]
    # You can replace the `for` loop with a dictionary comprehension:
    # how_many_dupes_left = {col: col_counter[col] for col in col_counter.keys()
    #                        if col_counter[col] > 1}
    return how_many_dupes_left


def make_column_names_unique(cols, max_len=64):
    """
    Replace duplicate column names with unique names.

    This returned list of unique names preserves the order of the original list
    of names.
    """
    new_cols = []

    # add a unique suffix to a column name only if it's duplicated.
    # the requirement to perserve the original order of the list complicates
    # the logic somewhat.
    cols_normalized = [normalize_column_name(col, max_len) for col in cols]
    how_many_of_each = count_occurrences(cols_normalized)
    how_many_dupes_left = \
        identify_duplicate_columns(cols_normalized)

    for col in reversed(cols_normalized):
        suffix = ''
        if col in how_many_dupes_left:
            digits = len(str(how_many_of_each[col]))
            num_padded = str(how_many_dupes_left[col]).zfill(digits)
            # num_padded = f'{dupe_counts[col]:0{digits}}'
            suffix = f'_{num_padded}'
            how_many_dupes_left[col] -= 1
        # if duplicate names have the max len, we need to truncate again before
        # appending the unique suffix
        truncation_pos = max_len - len(suffix)
        new_name = f'{col[:truncation_pos]}{suffix}'
        new_cols.insert(0, new_name)

    # Simple solution: add unique suffix to all column names
    # for i, col in enumerate(columns):
    #     suffix = f'_{i+1}'
    #     new_col = f'{col}{suffix}'
    #     new_columns.append(new_col)

    return new_cols
