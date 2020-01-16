"""
Integration tests for populate_facilities.py
"""

import populate_facilities


class TestPopulateFacilities:
    def test_populate_facilities(self):
        populate_facilities.main('health_care_facilities.csv')

    def test_deleteme(self):
        assert True
