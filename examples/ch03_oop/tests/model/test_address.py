"""
Unit tests for Address class.
"""

from manage_accounts.model.address import Address


def test_init_all_attributes() -> None:
    addr: Address = Address('123 Main St', 'Suite 101', 'Sacramento', 'CA', '94203', 'US')

    assert addr.street1 == '123 Main St'
    assert addr.street2 == 'Suite 101'
    assert addr.city == 'Sacramento'
    assert addr.state_province == 'CA'
    assert addr.postal_code == '94203'
    assert addr.country == 'US'


def test_init_street2_none() -> None:
    addr: Address = Address('123 Main St', None, 'Sacramento', 'CA', '94203', 'US')

    assert addr.street1 == '123 Main St'
    assert addr.street2 is None
    assert addr.city == 'Sacramento'
    assert addr.state_province == 'CA'
    assert addr.postal_code == '94203'
    assert addr.country == 'US'


def test_init_test_eq_true() -> None:
    addr1: Address = Address('123 Main St', 'Suite 101', 'Sacramento', 'CA', '94203', 'US')
    addr2: Address = Address('123 Main St', 'Suite 101', 'Sacramento', 'CA', '94203', 'US')

    assert addr1 == addr2


def test_init_test_eq_true() -> None:
    addr1: Address = Address('123 Main St', 'Suite 101', 'Sacramento', 'CA', '94203', 'US')
    addr2: Address = Address('123 Main St', 'Suite 101', 'Sacramento', 'CA', '94203', 'NZ')

    assert addr1 != addr2
