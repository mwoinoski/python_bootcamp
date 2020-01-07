"""
Unit tests for ETL data cleansing functions.
"""

from pytest import mark

from data_cleansing import normalize_column_name


def test_normalize_column_name_convert_upper_case_to_lower():
    result = normalize_column_name('STATE_PROVINCE')
    assert result == 'state_province'


def test_normalize_column_name_max_len():
    result = normalize_column_name('state_province', 10)
    assert result == 'state_prov'
