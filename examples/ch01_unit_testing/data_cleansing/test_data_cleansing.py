"""
Unit tests for ETL data cleansing functions.
"""

from pytest import mark

from data_cleansing import normalize_column_name

def setup_function():
    print('in setup_function')

def test_ccc_normalize_column_name_convert_upper_case_to_lower_leading_blanks():
    print('ccc')
    result = normalize_column_name('  STATE_PROVINCE  ')
    assert result == 'state_province'


def test_aaa_normalize_column_name_convert_upper_case_to_lower():
    print('aaa')
    result = normalize_column_name('STATE_PROVINCE')
    assert result == 'state_province'


def test_bbb_normalize_column_name_max_len():
    print('bbb')
    result = normalize_column_name('state_province', 10)
    assert result == 'state_prov'
