"""
Unit tests for Address class.
"""

from pytest import mark, raises
from facilities.address import Address


class TestAddress:
    def test_init_all_attributes(self):
        addr: Address = Address('123 Main St', 'Suite 101', 'Sacramento', 'CA', '94203')

        assert addr.street1 == '123 Main St'
        assert addr.street2 == 'Suite 101'
        assert addr.city == 'Sacramento'
        assert addr.state_province == 'CA'
        assert addr.postal_code == '94203'

    def test_init_street2_none(self):
        addr: Address = Address('123 Main St', None, 'Sacramento', 'CA', '94203')

        assert addr.street1 == '123 Main St'
        assert addr.street2 is None
        assert addr.city == 'Sacramento'
        assert addr.state_province == 'CA'
        assert addr.postal_code == '94203'
