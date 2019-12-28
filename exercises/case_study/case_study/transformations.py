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


def identify_duplicate_columns(cols: List[str], max_len: int) -> Dict[str, int]:
    pass


def make_column_names_unique(cols: List[str], max_len: int = 64) -> List[str]:
    """ Replace duplicate column names with unique names """
    new_cols: List[str] = []

    # add unique suffix to a column name only if it's duplicated
    cols_normalized = [normalize_column_name(col, max_len) for col in cols]
    how_many_of_each_col = Counter(cols_normalized)  # dictionary-like object
    dupe_counts: Dict[str, int] = {}
    for col in how_many_of_each_col:
        if how_many_of_each_col[col] > 1:
            dupe_counts[col] = how_many_of_each_col[col]
    # You can replace the `for` loop with a dictionary comprehension:
    # dupe_counts = {col: col_counter[col] for col in col_counter.keys()
    #                if col_counter[col] > 1}
    for col in reversed(cols_normalized):
        suffix: str = ''
        if col in dupe_counts.keys():
            digits = len(str(how_many_of_each_col[col]))
            num_padded: str = str(dupe_counts[col]).zfill(digits)
            # num_padded: str = f'{dupe_counts[col]:0{digits}}'
            suffix = f'_{num_padded}'
            dupe_counts[col] -= 1
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
