"""
Transformation functions for ETL procesing.
"""
from collections import Counter
import re
from typing import List, Dict


def normalize_column_name(name: str, max_len: int) -> str:
    name = name.lower()
    name = re.sub(r'\W', '_', name)
    name = name.strip('_')
    name = name[:max_len]
    return name


def count_occurrences(cols: List[str]) -> Dict[str, int]:
    """
    Return a dictionary of (column-name, number-of-occurences).
    Assumes the names in the argument list have been normalized.
    """
    return dict(Counter(cols))  # Counter is a dictionary-like object


def identify_duplicate_columns(
        cols: List[str], how_many: Dict[str, int] = None) -> Dict[str, int]:
    if not how_many:
        how_many = count_occurrences(cols)
    how_many_dupes_left: Dict[str, int] = {}
    for col in how_many:
        if how_many[col] > 1:
            how_many_dupes_left[col] = how_many[col]
    # You can replace the `for` loop with a dictionary comprehension:
    # how_many_dupes_left = {col: col_counter[col] for col in col_counter.keys()
    #                        if col_counter[col] > 1}
    return how_many_dupes_left


def make_column_names_unique(cols: List[str], max_len: int = 64) -> List[str]:
    """
    Replace duplicate column names with unique names.
    This returned list of unique names perserves the order of the original list
    of names.
    """
    new_cols: List[str] = []

    # add a unique suffix to a column name only if it's duplicated.
    # the requirement to perserve the original order of the list complicates
    # the logic somewhat.
    cols_normalized = [normalize_column_name(col, max_len) for col in cols]
    how_many_of_each = count_occurrences(cols_normalized)
    how_many_dupes_left: Dict[str, int] = \
        identify_duplicate_columns(cols_normalized)

    for col in reversed(cols_normalized):
        suffix: str = ''
        if col in how_many_dupes_left:
            digits = len(str(how_many_of_each[col]))
            num_padded: str = str(how_many_dupes_left[col]).zfill(digits)
            # num_padded: str = f'{dupe_counts[col]:0{digits}}'
            suffix = f'_{num_padded}'
            how_many_dupes_left[col] -= 1
        # if duplicate names have the max len, we need to truncate again before
        # appending the unique suffix
        truncation_pos = max_len - len(suffix)
        new_name: str = f'{col[:truncation_pos]}{suffix}'
        new_cols.insert(0, new_name)

    # Simple solution: add unique suffix to all column names
    # for i, col in enumerate(columns):
    #     suffix: str = f'_{i+1}'
    #     new_col: str = f'{col}{suffix}'
    #     new_columns.append(new_col)

    return new_cols
