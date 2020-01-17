"""
Test cases for find_dupe_cert_nums.py
"""

import find_dupe_cert_nums


# TODO: note the following test case of the code in find_dupe_cert_nums.py
# (no code changes requierd)
def test_multiple_records_some_dupes() -> None:

    filepath = 'facility_perf_scores.csv'

    dupes = find_dupe_cert_nums.main(filepath)

    assert dupes == 2
