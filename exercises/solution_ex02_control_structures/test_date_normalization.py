"""
Unit test cases for date normalization functions.
"""

from pytest import mark  # required for @mark.skip

from date_normalization import normalize_date, is_leap_year


# TODO: Run the tests in this file using pytest.

def test_normalize_date_ymd():
    date = '2021-01-25'
    result = normalize_date(date)
    assert result == '2021-01-25'


# TODO: after you get the first test case running, delete the following
#       @mark.skip decorator and run pytest again
# @mark.skip
def test_normalize_date_dmy():
    date = '25/01/2021'
    result = normalize_date(date, 'DMY')
    assert result == '2021-01-25'


# @mark.skip
def test_normalize_date_mdy():
    date = '01/25/2021'
    result = normalize_date(date, 'MDY')
    assert result == '2021-01-25'


# @mark.skip
def test_normalize_date_invalid_format():
    date = '01/25/2021'
    result = normalize_date(date, 'YDM')
    assert result is None


# @mark.skip
def test_normalize_date_dmy_two_digit_year():
    date = '25/01/21'
    result = normalize_date(date, 'DMY')
    assert result == '2021-01-25'


# @mark.skip
def test_normalize_date_mdy_two_digit_year():
    date = '01/25/21'
    result = normalize_date(date, 'MDY')
    assert result == '2021-01-25'


# @mark.skip
def test_normalize_date_mdy_month_0():
    date = '00/25/2021'
    result = normalize_date(date, 'MDY')
    assert result is None


# @mark.skip
def test_normalize_date_mdy_month_13():
    date = '13/25/2021'
    result = normalize_date(date, 'MDY')
    assert result is None


# @mark.skip
def test_normalize_date_dmy_month_0():
    date = '25/00/2021'
    result = normalize_date(date, 'DMY')
    assert result is None


# @mark.skip
def test_normalize_date_dmy_month_13():
    date = '25/13/2021'
    result = normalize_date(date, 'DMY')
    assert result is None


# @mark.skip
def test_normalize_date_mdy_invalid_day():
    date = '04/31/2021'
    result = normalize_date(date, 'MDY')
    assert result is None


# @mark.skip
def test_normalize_date_mdy_feb_29_non_leap_year():
    date = '02/29/2021'
    result = normalize_date(date, 'MDY')
    assert result is None


# @mark.skip
def test_normalize_date_mdy_feb_29_leap_year():
    date = '02/29/2020'
    result = normalize_date(date, 'MDY')
    assert result == '2020-02-29'


# @mark.skip
@mark.parametrize('year, expected', [
    (2020, True),
    (2019, False),
    (2100, False),
    (2000, True),
])
def test_is_leap_year(year, expected):
    assert is_leap_year(year) == expected
