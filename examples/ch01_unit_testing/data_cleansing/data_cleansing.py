"""
Functions for data cleansing during ETL processing.
"""

import re


def normalize_column_name(name, max_len=64):
    """ Return a normalized version of the column name """
    name = name.lower()
    name = re.sub(r'\W+', '_', name)
    name = name.strip('_')
    name = name[0:max_len]
    return name
