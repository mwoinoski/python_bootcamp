"""
Unit test cases for Facility class
"""

from facilities.facility import Facility


class TestFacility:
    def test_init(self) -> None:

        facility = Facility(98765, 'Best Care', '123 Wellness Blvd Sacramento CA 93253')

        assert facility.name == 'Best Care'
        assert facility.cert_number == 98765
        assert facility.address == '123 Wellness Blvd Sacramento CA 93253'

    def test_dunder_str(self) -> None:
        facility = Facility(98765, 'Best Care', '123 Wellness Blvd Sacramento CA 93253')

        assert str(facility) == 'Best Care'  # str(facility) calls facility.__str__()
