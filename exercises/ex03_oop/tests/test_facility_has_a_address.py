"""
Unit tests for Address class.
"""

from facilities.address import Address
from facilities.facility import Facility


class TestFacilityHasAnAddress:
    # TODO: modify the Facility class __init__ method by changing the type of the
    #       address argument from str to Address

    def test_init(self) -> None:
        # TODO: note how we create an Address object
        addr: Address = Address('123 Main St', 'Sacramento', 'CA', '94203')

        # TODO: note how we pass the Address argument to the Facility constructor
        facility = Facility(98765, 'Best Care', addr)

        assert facility.name == 'Best Care'
        assert facility.cert_number == 98765
        # TODO: note how we access the Address of the Facility by chaining
        #       attribute references: facility.address.street
        assert facility.address.street == '123 Main St'
        assert facility.address.city == 'Sacramento'
        assert facility.address.state == 'CA'
        assert facility.address.zip_code == '94203'
