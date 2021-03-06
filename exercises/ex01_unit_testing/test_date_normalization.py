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
    assert is_leap_year(2020)


# TODO: write a test case that verifies that 2019 was not a leap year
def test_is_leap_year_not_multiple_of_four():
    ....


# TODO: write a test case that verifies that 2100 will not be a leap year
def ....
    ....


# TODO: write a test case that verifies that 2000 was a leap year
def ....
    ....


# BONUS TODO: write a single parameterized test case that performs the same
#             tests as the above four separate test functions.
# HINT: See page 27 in the course notes
