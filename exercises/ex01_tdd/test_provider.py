"""
Unit tests for provider functions.
"""


from pytest import mark, raises

from provider import is_valid_npi


def test_is_valid_npi_true() -> None:
    assert is_valid_npi("1234567893")
    assert is_valid_npi("2234567891")
    assert is_valid_npi("1000000004")
    assert is_valid_npi("2000000002")
    assert is_valid_npi("1345678902")


def test_is_valid_npi_none_false() -> None:
    assert not is_valid_npi(None)


# TODO: remove the skip decorator, then modify provider.py so this test passes
# @mark.skip
def test_is_valid_npi_empty_false() -> None:
    assert not is_valid_npi("")


# TODO: remove the skip decorator, then modify provider.py so this test passes
# @mark.skip
def test_is_valid_npi_too_short_false() -> None:
    assert not is_valid_npi("123456789")


# TODO: remove the skip decorator, then modify provider.py so this test passes
# @mark.skip
def test_is_valid_npi_too_long_true() -> None:
    assert not is_valid_npi("12234567893")


# TODO: remove the skip decorator, then modify provider.py so this test passes
# @mark.skip
def test_is_valid_npi_does_not_start_with_1_or_2_false() -> None:
    assert not is_valid_npi("3234567893")


# TODO: remove the skip decorator, then modify provider.py so this test passes
# @mark.skip
def test_is_valid_npi_contains_letter_false() -> None:
    assert not is_valid_npi("2a34567893")


# TODO: remove the skip decorator, then modify provider.py so this test passes
# @mark.skip
def test_is_valid_npi_contains_commas_false() -> None:
    assert not is_valid_npi("23,456,783")


# TODO: remove the skip decorator, then modify provider.py so this test passes
# @mark.skip
def test_is_valid_npi_bad_check_digit_false() -> None:
    assert not is_valid_npi("2234567893")


# TODO: replace all the tests above with a single parameterized test case
# @mark.skip
@mark.parametrize(
    "npi, expected_result", [
        (None, False),           # can't be None
        ("", False),             # too short
        ("123456789", False),    # too short
        ("12234567893", False),  # too long
        ("3234567893", False),   # doesn't start with 1 or 2
        ("2a34567893", False),   # non-numeric character
        ("23,456,783", False),   # non-numeric character
        ("2234567893", False),   # bad check digit
        ("1234567893", True),
        ("2234567891", True),
        ("1000000004", True),
        ("2000000002", True),
        ("1345678902", True),
    ])
def test_is_valid_npi(npi: str, expected_result: bool) -> None:
    assert is_valid_npi(npi) == expected_result
