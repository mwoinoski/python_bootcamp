"""
Unit tests for ETL data cleansing functions.
"""

from pytest import mark

from data_cleansing import normalize_column_name


@mark.parametrize('name, max_len, expected', [
    ('state province', 64, 'state_province'),
    ('STATE PROVINCE', 64, 'state_province'),
    ('state/province', 64, 'state_province'),
    ('state_province_', 64, 'state_province'),
    ('  state province  ', 64, 'state_province'),
    ('state province', 10, 'state_prov'),
])
def test_normalize_column_name(name, max_len, expected):
    result = normalize_column_name(name, max_len)

    assert result == expected
