"""
Unit tests for transformation logic
"""

from pytest import mark
from typing import List, Dict
from unittest import main, TestCase

from case_study.transformations import (
    make_column_names_unique, normalize_column_name, identify_duplicate_columns
)


class MyTestCase(TestCase):
    # def test_make_column_names_unique_no_dupes(self) -> None:
    #     cols: List[str] = ['first', 'second', 'third', 'fourth', 'fifth']
    #     expected: List[str] = ['first_001', 'second_002', 'third_003', 'fourth_004', 'fifth_005']
    #
    #     actual: List[str] = make_column_names_unique(cols)
    #
    #     assert actual == expected

    # def test_make_column_names_unique_dupes(self) -> None:
    #     cols: List[str] = ['first', 'second', 'third', 'second', 'fifth']
    #     expected: List[str] = ['first_001', 'second_002', 'third_003', 'second_004', 'fifth_005']
    #
    #     actual: List[str] = make_column_names_unique(cols)
    #
    #     assert actual == expected

    def test_make_column_names_unique_no_dupes(self) -> None:
        cols: List[str] = ['first', 'second', 'third', 'fourth', 'fifth']
        expected: List[str] = ['first', 'second', 'third', 'fourth', 'fifth']

        actual: List[str] = make_column_names_unique(cols)

        assert actual == expected

    def test_make_column_names_unique_dupes(self) -> None:
        cols: List[str] = ['first', 'second', 'third', 'second', 'third', 'fourth']
        expected: List[str] = ['first', 'second_1', 'third_1', 'second_2', 'third_2', 'fourth']

        actual: List[str] = make_column_names_unique(cols)

        assert actual == expected

    def test_make_column_names_unique_dupes_different_case(self) -> None:
        cols: List[str] = ['first', 'second', 'third', 'SECOND', 'Third', 'fourth']
        expected: List[str] = ['first', 'second_1', 'third_1', 'second_2', 'third_2', 'fourth']

        actual: List[str] = make_column_names_unique(cols)

        assert actual == expected

    def test_make_column_names_unique_dupes_two_digit_suffix(self) -> None:
        cols: List[str] = ['x', 'y'] + ['a'] * 20
        expected: List[str] = ['x', 'y'] + [f'a_{i:02d}' for i in range(1, 21)]

        actual: List[str] = make_column_names_unique(cols)

        assert actual == expected

    def test_make_column_names_unique_dupes_three_digit_suffix(self) -> None:
        cols: List[str] = ['x', 'y'] + ['a'] * 200
        expected: List[str] = ['x', 'y'] + [f'a_{i:03d}' for i in range(1, 201)]

        actual: List[str] = make_column_names_unique(cols)

        assert actual == expected

    def test_make_column_names_unique_dupes_after_truncation(self) -> None:
        cols: List[str] = ['domain_score', 'domain_score_unweighted']
        expected: List[str] = ['domain_s_1', 'domain_s_2']

        actual: List[str] = make_column_names_unique(cols, max_len=10)

        assert actual == expected

    def test_make_column_names_unique_dupe_after_trunc_boundary(self) -> None:
        cols: List[str] = ['domain_score', 'domain_score_unweighted']
        expected: List[str] = ['domain_sco_1', 'domain_sco_2']

        actual: List[str] = make_column_names_unique(cols, max_len=12)

        assert actual == expected

    def test_make_column_names_unique_dupe_max_len_minus_one(self) -> None:
        cols: List[str] = ['domain_score', 'domain_score']
        expected: List[str] = ['domain_scor_1', 'domain_scor_2']

        actual: List[str] = make_column_names_unique(cols, max_len=13)

        assert actual == expected

    def test_make_column_names_unique_last_char_is_underscore(self) -> None:
        cols: List[str] = ['domain_score_', 'domain_score_']
        expected: List[str] = ['domain_score_1', 'domain_score_2']

        actual: List[str] = make_column_names_unique(cols, max_len=15)

        assert actual == expected

    def test_make_column_names_unique_last_char_after_truncation_is_underscore(self) -> None:
        cols: List[str] = ['domain_score_min', 'domain_score_max']
        expected: List[str] = ['domain_scor_1', 'domain_scor_2']

        actual: List[str] = make_column_names_unique(cols, max_len=13)

        assert actual == expected

    def test_make_column_names_unique_dupe_one_and_two_digit_suffix(self) -> None:
        """
        Tricky case: if there are 10 or more duplicates, we want the prefix
        to be the same for all names, even if the length of the resulting names
        is different; e.g., 'domain_sc_09' and 'domain_sc_10', not
        'domain_sco_9' and 'domain_sc_10'
        """
        cols: List[str] = ['domain_score'] * 10 + ['state'] * 9
        expected: List[str] = [f'domain_sc_{i:02d}' for i in range(1, 11)] + \
                              [f'state_{i}' for i in range(1, 10)]

        actual: List[str] = make_column_names_unique(cols, max_len=12)

        assert actual == expected

    @mark.skip("""TODO""")
    def test_identify_duplicate_columns_after_normalization(self) -> None:
        cols: List[str] = [
            'domain_score', 'state', 'city', 'country', 'street1', 'street2',
            'domain_score', 'state', 'city',
            'domain_score_max', 'domain_score_min',
        ]
        expected: Dict[str, int] = {
            'domain_score': 4,
            'state': 2,
            'city': 2
        }

        actual: Dict[str, int] = identify_duplicate_columns(cols, max_len=12)

        assert actual == expected

    @mark.skip("""TODO""")
    def test_supply_mappings_for_duplicate_column_names(self) -> None:
        pass


@mark.parametrize('name, max_len, expected', [
    ('state province', 64, 'state_province'),
    ('state/province', 64, 'state_province'),
    ('STATE PROVINCE', 64, 'state_province'),
    ('state-province', 64, 'state_province'),
    ('state_province_', 64, 'state_province'),
    ('state province', 64, 'state_province'),
    ('  state province  ', 64, 'state_province'),
    ('state province', 10, 'state_prov'),
])
def test_normalize_column_names(name, max_len, expected) -> None:
    assert expected == normalize_column_name(name, max_len)


if __name__ == '__main__':
    main()
