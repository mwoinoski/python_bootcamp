"""
Unit tests for InPatientRehab class.
"""

from facilities.dialysis_facility import DialysisFacility


class TestDialysisFacility:
    def test_init(self) -> None:

        facility = DialysisFacility(98765, 'Acme Dialysis',
                                    '123 Wellness Blvd Sacramento CA 93253', 40)

        assert facility.name == 'Acme Dialysis'
        assert facility.cert_number == 98765
        assert facility.address == '123 Wellness Blvd Sacramento CA 93253'
        assert facility.number_of_dialysis_machines == 40

    def test_dunder_str(self) -> None:
        facility = DialysisFacility(98765, 'Acme Dialysis',
                                    '123 Wellness Blvd Sacramento CA 93253', 40)

        assert str(facility) == 'Acme Dialysis: 40 dialysis machines'

    def test_calculate_quality_score(self) -> None:
        facility = DialysisFacility(98765, 'Acme Dialysis',
                                    '123 Wellness Blvd Sacramento CA 93253', 40)

        score = facility.calculate_quality_score()
        assert score == 120
