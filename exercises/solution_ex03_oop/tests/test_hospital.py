"""
Unit tests for Hospital class.
"""

from facilities.hospital import Hospital


class TestHospital:
    def test_init(self) -> None:

        hospital = Hospital(98765, 'General Hospital',
                            '123 Wellness Blvd Sacramento CA 93253', 45)

        assert hospital.name == 'General Hospital'
        assert hospital.cert_number == 98765
        assert hospital.address == '123 Wellness Blvd Sacramento CA 93253'
        assert hospital.number_of_beds == 45

    def test_dunder_str(self) -> None:
        hospital = Hospital(98765, 'General Hospital',
                            '123 Wellness Blvd Sacramento CA 93253', 45)

        assert str(hospital) == 'General Hospital: 45 beds'

    def test_calculate_quality_score(self) -> None:
        hospital = Hospital(98765, 'General Hospital',
                            '123 Wellness Blvd Sacramento CA 93253', 45)

        score = hospital.calculate_quality_score()
        assert score == 90
