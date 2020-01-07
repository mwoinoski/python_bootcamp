"""
Unit tests for Provider class.
"""

from pytest import mark, raises

from person.provider import Provider


def test_init_success() -> None:
    p: Provider = Provider("1234567893", "Lee", "Mary", "")

    assert ("1234567893", "Mary", "", "Lee") == \
           (p.npi, p.given_name, p.middle_name, p.family_name)


def test_init_bad_npi_raises_exception() -> None:
    with raises(ValueError, match=r"NPI.*(in|not\s+)valid"):
        Provider("Lee", "", "1234567892", "Mary")


def test_npi_is_private() -> None:
    p: Provider = Provider("1234567893", "Lee", "", "Mary")

    with raises(AttributeError, match="can't set attribute"):
        p.npi = "2234567891"


# def test_is_valid_npi() -> None:
#     assert Provider.is_valid_npi("1234567893")
#     assert Provider.is_valid_npi("2234567891")
#     assert Provider.is_valid_npi("1000000004")
#     assert Provider.is_valid_npi("2000000002")
#     assert Provider.is_valid_npi("1345678902")
#     assert not Provider.is_valid_npi(None)
#     assert not Provider.is_valid_npi("")
#     assert not Provider.is_valid_npi("123456789")
#     assert not Provider.is_valid_npi("12234567893")
#     assert not Provider.is_valid_npi("3234567893")
#     assert not Provider.is_valid_npi("2234567893")
#     assert not Provider.is_valid_npi("2a34567893")
#     assert not Provider.is_valid_npi("23,456,783")


@mark.parametrize(
    "npi, expected_result", [
        ("1234567893", True),
        ("2234567891", True),
        ("1000000004", True),
        ("2000000002", True),
        ("1345678902", True),
        (None, False),           # can't be None
        ("", False),             # too short
        ("123456789", False),    # too short
        ("12234567893", False),  # too long
        ("3234567893", False),   # doesn't start with 1 or 2
        ("2234567893", False),   # bad check digit
        ("2a34567893", False),   # non-numeric character
        ("23,456,783", False),   # non-numeric character
    ])
def test_is_valid_npi(npi: str, expected_result: bool) -> None:
    assert Provider.is_valid_npi(npi) == expected_result
