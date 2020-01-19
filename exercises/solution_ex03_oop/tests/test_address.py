"""
Unit tests for Address class.
"""

from facilities.address import Address


class TestAddress:
    def test_init_all_attributes(self):
        addr: Address = Address('123 Main St', 'Sacramento', 'CA', '94203')

        assert addr.street == '123 Main St'
        assert addr.city == 'Sacramento'
        assert addr.state == 'CA'
        assert addr.zip_code == '94203'

    def test_dunder_str(self):
        addr: Address = Address('123 Main St', 'Sacramento', 'CA', '94203')

        assert str(addr) == '123 Main St Sacramento CA 94203'
