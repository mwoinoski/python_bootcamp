"""
Integration tests for populate_facilities.py
"""
from typing import List

from facilities.facility import Facility
from facilities.hospital import Hospital
from facilities.dialysis_facility import DialysisFacility


class TestPopulateFacilities:
    def test_populate_facilities(self):
        facilities: List[Facility] = [
            DialysisFacility(98765, 'Acme Dialysis',
                             '123 Renal Rd Sacramento CA 93253', 40),
            Hospital(98765, 'General Hospital',
                     '234 Wellness Blvd Sacramento CA 93253', 40),
            DialysisFacility(98765, 'Top Notch Dialysis',
                             '123 Renal Rd Sacramento CA 93253', 40),
            Hospital(98765, 'Community Hospital',
                     '234 Wellness Blvd Sacramento CA 93253', 40)
        ]

        for i, expected_score in enumerate([120, 80, 120, 80]):
            assert facilities[i].calculate_quality_score() == expected_score
