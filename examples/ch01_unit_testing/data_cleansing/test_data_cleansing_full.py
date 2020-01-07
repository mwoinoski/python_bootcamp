"""
Unit tests for ETL data cleansing functions.
"""

from pytest import mark

from data_cleansing import normalize_column_name


def test_normalize_column_name_already_normalized():
    result = normalize_column_name('state_province')
    assert result == 'state_province'


def test_normalize_column_name_convert_upper_case_to_lower():
    result = normalize_column_name('STATE_PROVINCE')
    assert result == 'state_province'


def test_normalize_column_name_replace_space_with_underscore():
    result = normalize_column_name('state province')
    assert result == 'state_province'


def test_normalize_column_name_replace_multiple_spaces():
    result = normalize_column_name('state   province')
    assert result == 'state_province'


def test_normalize_column_name_replace_slash_with_underscore():
    result = normalize_column_name('state/province')
    assert result == 'state_province'


def test_normalize_column_name_replace_dash_with_underscore():
    result = normalize_column_name('state-province')
    assert result == 'state_province'


def test_normalize_column_name_strip_leading_and_trailing_whitespace():
    result = normalize_column_name('  state_province  ')
    assert result == 'state_province'


def test_normalize_column_name_max_len():
    result = normalize_column_name('state_province', 10)
    assert result == 'state_prov'


def test_normalize_column_name_max_len_threshold_minus_1():
    result = normalize_column_name('state_province', 15)
    assert result == 'state_province'


def test_normalize_column_name_max_len_threshold_exactly():
    result = normalize_column_name('state_province', 14)
    assert result == 'state_province'


def test_normalize_column_name_max_len_threshold_plus_1():
    result = normalize_column_name('state_province', 13)
    assert result == 'state_provinc'


def test_normalize_column_name_max_len_do_not_leave_trailing_underscore():
    result = normalize_column_name('state_', 6)
    assert result == 'state'


def test_normalize_column_name_len_1():
    result = normalize_column_name('x')
    assert result == 'x'


# TODO raise exception if name is empty
# def test_normalize_column_name_len_0():
#     pass


# TODO raise exception if name is None
# def test_normalize_column_name_arg_is_none():
#     pass


# TODO raise exception if max_len < 1
# def test_normalize_column_name_max_len_zero():
#     pass
