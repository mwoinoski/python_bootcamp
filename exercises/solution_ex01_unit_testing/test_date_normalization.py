"""
Unit test cases for data normalization functions.
"""

from pytest import mark  # required for @mark.skip

from data_normalization import is_leap_year


# TODO: note the rules for leap years:
#       A year is leap year if it's a multiple of 4 and
#       (it's not a multiple of 100 or it's a multiple of 400)


# TODO: complete the following test case so it verifies that 2020 is a leap year
def test_is_leap_year_multiple_of_four():
    # Arrange

    # Act
    is_leap = is_leap_year(2020)

    # Assert
    assert is_leap


# TODO: write a test case that verifies that 2019 was not a leap year
def test_is_leap_year_not_multiple_of_four():
    assert not is_leap_year(2019)


# TODO: write a test case that verifies that 2100 will not be a leap year
def test_is_leap_year_century_not_multiple_of_four_hundred():
    assert not is_leap_year(2100)


# TODO: write a test case that verifies that 2000 was a leap year
def test_is_leap_year_century_multiple_of_four_hundred():
    assert is_leap_year(2000)


# BONUS TODO: write a single parameterized test case that performs the same
#             tests as the above four separate test functions.
# HINT: See page 27 in the course notes
@mark.parametrize('year, expected', [
    (2020, True),
    (2019, False),
    (2100, False),
    (2000, True),
])
def test_is_leap_year(year, expected):
    assert is_leap_year(year) == expected
