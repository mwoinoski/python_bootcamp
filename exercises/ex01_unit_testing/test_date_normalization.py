"""
Unit test cases for data normalization functions.
"""

from pytest import mark  # required for @mark.skip

from date_normalization import is_leap_year


def test_is_leap_year_multiple_of_four():
    assert is_leap_year(2020)


def test_is_leap_year_not_multiple_of_four():
    assert not is_leap_year(2019)


def test_is_leap_year_century_not_multiple_of_four_hundred():
    assert not is_leap_year(2100)


def test_is_leap_year_century_multiple_of_four_hundred():
    assert is_leap_year(2000)


@mark.parametrize('year, expected', [
    (2020, True),
    (2019, False),
    (2100, False),
    (2000, True),
])
def test_is_leap_year(year, expected):
    assert is_leap_year(year) == expected
