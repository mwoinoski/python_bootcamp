"""
Unit tests for transformation logic
"""
from datetime import datetime
from typing import List, Dict, Any
import pytest
from pytest import mark

from case_study.etl.transform.transformer import Transformer


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
# pylint: disable=missing-function-docstring
def test_normalize_column_names(name, max_len, expected) -> None:
    assert expected == Transformer().normalize_column_name(name, max_len)


@mark.parametrize('date_str, expected, date_format', [
    ('2020-01-02', '2020-01-02', None),  # ISO 8701 YMD (Year-Month-Day) format
    ('2020/01/02', '2020-01-02', None),
    ('2020/1/2', '2020-01-02', None),
    (' 2020-01-02 ', '2020-01-02', None),
    ('2020-01-02', '2020-01-02', Transformer.DateFormat.YMD),
    ('01/02/2020', '2020-01-02', Transformer.DateFormat.MDY),
    ('1/2/2020', '2020-01-02', Transformer.DateFormat.MDY),
    ('01/02/20', '2020-01-02', Transformer.DateFormat.MDY),
    ('1/2/20', '2020-01-02', Transformer.DateFormat.MDY),
    ('02/01/2020', '2020-01-02', Transformer.DateFormat.DMY),
    ('2/1/2020', '2020-01-02', Transformer.DateFormat.DMY),
    ('02/01/20', '2020-01-02', Transformer.DateFormat.DMY),
    ('2/1/20', '2020-01-02', Transformer.DateFormat.DMY),
    ('1/2/20/20', '', Transformer.DateFormat.MDY),
    ('1/2', '', Transformer.DateFormat.MDY),
    ('1/2/020', '', Transformer.DateFormat.MDY),
    ('1/2/20202', '', Transformer.DateFormat.MDY),
    ('222/1/2020', '', Transformer.DateFormat.MDY),
    ('2/29/2020', '2020-02-29', Transformer.DateFormat.MDY),
    ('2/29/2021', '', Transformer.DateFormat.MDY),
    ('January 2, 2020', '', Transformer.DateFormat.MDY),
    ('2 Jan 2020', '', Transformer.DateFormat.MDY),
    ('1/2/2020 12:34', '', Transformer.DateFormat.MDY),
    ('1/2/2020 12:34 PM', '', Transformer.DateFormat.MDY),
    ('2019-12-28T14:27:25', '', Transformer.DateFormat.MDY),  # ISO 8601
    ('2019-12-28T14:27:25+00:00', '', Transformer.DateFormat.MDY),  # ISO 8601 with timezone info
    ('2019-12-28T14:27:25', '', Transformer.DateFormat.MDY),  # ISO 8601
    ('2019-12-28T14:27:25Z', '', Transformer.DateFormat.MDY),  # ISO 8601 (Z == GMT/UTC)
    ('20191228T142725Z', '', Transformer.DateFormat.MDY),  # ISO 8601 with timezone
    ('--01-02', '', Transformer.DateFormat.MDY),  # ISO 8601 date without a year
    ('', '', Transformer.DateFormat.MDY),  # ISO 8601
    ('', '', None),
    (None, '', None),
])
# pylint: disable=missing-function-docstring
def test_normalize_dates(
        date_str: str, expected: str, date_format: Any) -> None:
    if not date_format:
        assert Transformer().normalize_date(date_str) == expected
    else:
        assert Transformer().normalize_date(date_str, date_format) == expected


# pylint: disable=missing-function-docstring
def test_normalize_dates_bad_date_format() -> None:
    with pytest.raises(ValueError):
        Transformer().normalize_date('20/1/2', 'YDM')


@mark.parametrize('date, expected', [
    (datetime(2020, 1, 2), '2020-01-02T00:00:00'),
    (datetime(2020, 1, 2, 12, 34), '2020-01-02T12:34:00'),
    (datetime(2020, 1, 2, 12, 34, 56), '2020-01-02T12:34:56'),
    (datetime(2020, 1, 2, 12, 34, 56, 123456), '2020-01-02T12:34:56'),
    (None, ''),
    ('', ''),
])
# pylint: disable=missing-function-docstring
def test_convert_date_to_timestamp(date: datetime, expected: str) -> None:
    assert Transformer().convert_date_to_timestamp(date) == expected


@mark.parametrize('year_str, expected', [
    ('2020', 2020),
    ('80', 2080),
    ('202', 0),
    ('1889', 0),
    ('1890', 1890),
    ('1891', 1891),
    ('2149', 2149),
    ('2150', 2150),
    ('2151', 0),
    (None, 0),
    ('', 0),
])
# pylint: disable=missing-function-docstring
def test_get_valid_year(year_str: str, expected: int) -> None:
    assert Transformer().get_valid_year(year_str) == expected


class TransformationsTest:
    """ Unit test cases for functions in transformer.py """

    # def test_make_column_names_unique_no_dupes(self) -> None:
    #     cols: List[str] = ['first', 'second', 'third', 'fourth', 'fifth']
    #     expected: List[str] = ['first_001', 'second_002', 'third_003',
    #                            'fourth_004', 'fifth_005']
    #
    #     actual: List[str] = Transformer(). make_column_names_unique(cols)
    #
    #     assert actual == expected

    # def test_make_column_names_unique_dupes(self) -> None:
    #     cols: List[str] = ['first', 'second', 'third', 'second', 'fifth']
    #     expected: List[str] = ['first_001', 'second_002', 'third_003',
    #                            'second_004', 'fifth_005']
    #
    #     actual: List[str] = Transformer(). make_column_names_unique(cols)
    #
    #     assert actual == expected

    # pylint: disable=no-self-use,missing-function-docstring
    def test_make_column_names_unique_no_dupes(self) -> None:
        cols: List[str] = ['first', 'second', 'third', 'fourth', 'fifth']
        expected: List[str] = ['first', 'second', 'third', 'fourth', 'fifth']

        actual: List[str] = Transformer().make_column_names_unique(cols)

        assert actual == expected

    # pylint: disable=no-self-use,missing-function-docstring
    def test_make_column_names_unique_dupes(self) -> None:
        cols: List[str] = ['first', 'second', 'third', 'second',
                           'third', 'fourth']
        expected: List[str] = ['first', 'second_1', 'third_1', 'second_2',
                               'third_2', 'fourth']

        actual: List[str] = Transformer().make_column_names_unique(cols)

        assert actual == expected

    # pylint: disable=no-self-use,missing-function-docstring
    def test_make_column_names_unique_dupes_different_case(self) -> None:
        cols: List[str] = ['first', 'second', 'third', 'SECOND',
                           'Third', 'fourth']
        expected: List[str] = ['first', 'second_1', 'third_1', 'second_2',
                               'third_2', 'fourth']

        actual: List[str] = Transformer().make_column_names_unique(cols)

        assert actual == expected

    # pylint: disable=no-self-use,missing-function-docstring
    def test_make_column_names_unique_dupes_two_digit_suffix(self) -> None:
        cols: List[str] = ['x', 'y'] + ['a'] * 20
        expected: List[str] = ['x', 'y'] + [f'a_{i:02d}' for i in range(1, 21)]

        actual: List[str] = Transformer().make_column_names_unique(cols)

        assert actual == expected

    # pylint: disable=no-self-use,missing-function-docstring
    def test_make_column_names_unique_dupes_three_digit_suffix(self) -> None:
        cols: List[str] = ['x', 'y'] + ['a'] * 200
        expected: List[str] = ['x', 'y'] + [f'a_{i:03d}' for i in range(1, 201)]

        actual: List[str] = Transformer().make_column_names_unique(cols)

        assert actual == expected

    # pylint: disable=no-self-use,missing-function-docstring
    def test_make_column_names_unique_dupes_after_truncation(self) -> None:
        cols: List[str] = ['domain_score', 'domain_score_unweighted']
        expected: List[str] = ['domain_s_1', 'domain_s_2']

        actual: List[str] = Transformer().make_column_names_unique(cols, max_len=10)

        assert actual == expected

    # pylint: disable=no-self-use,missing-function-docstring
    def test_make_column_names_unique_dupe_after_trunc_boundary(self) -> None:
        cols: List[str] = ['domain_score', 'domain_score_unweighted']
        expected: List[str] = ['domain_sco_1', 'domain_sco_2']

        actual: List[str] = Transformer().make_column_names_unique(cols, max_len=12)

        assert actual == expected

    # pylint: disable=no-self-use,missing-function-docstring
    def test_make_column_names_unique_dupe_max_len_minus_one(self) -> None:
        cols: List[str] = ['domain_score', 'domain_score']
        expected: List[str] = ['domain_scor_1', 'domain_scor_2']

        actual: List[str] = Transformer().make_column_names_unique(cols, max_len=13)

        assert actual == expected

    # pylint: disable=no-self-use,missing-function-docstring
    def test_make_column_names_unique_last_char_is_underscore(self) -> None:
        cols: List[str] = ['domain_score_', 'domain_score_']
        expected: List[str] = ['domain_score_1', 'domain_score_2']

        actual: List[str] = Transformer(). make_column_names_unique(cols, max_len=15)

        assert actual == expected

    # pylint: disable=no-self-use,missing-function-docstring
    def test_make_column_names_unique_last_char_after_truncation_is_underscore(
            self) -> None:
        cols: List[str] = ['domain_score_min', 'domain_score_max']
        expected: List[str] = ['domain_scor_1', 'domain_scor_2']

        actual: List[str] = Transformer(). make_column_names_unique(cols, max_len=13)

        assert actual == expected

    # pylint: disable=no-self-use,missing-function-docstring
    def test_make_column_names_unique_dupe_one_and_two_digit_suffix(
            self) -> None:
        """
        Tricky case: if there are 10 or more duplicates, we want the prefix
        to be the same for all names, even if the length of the resulting names
        is different; e.g., 'domain_sc_09' and 'domain_sc_10', not
        'domain_sco_9' and 'domain_sc_10'
        """
        cols: List[str] = ['domain_score'] * 10 + ['state'] * 9
        expected: List[str] = [f'domain_sc_{i:02d}' for i in range(1, 11)] + \
                              [f'state_{i}' for i in range(1, 10)]

        actual: List[str] = Transformer(). make_column_names_unique(cols, max_len=12)

        assert actual == expected

    # pylint: disable=no-self-use,missing-function-docstring
    def test_identify_duplicate_columns_after_normalization(self) -> None:
        cols: List[str] = [
            'domain_score', 'state', 'city', 'country', 'street1', 'street2',
            'domain_score', 'state', 'city',
            'domain_score', 'domain_score',
        ]
        expected: Dict[str, int] = {
            'domain_score': 4,
            'state': 2,
            'city': 2
        }

        actual: Dict[str, int] = Transformer().identify_duplicate_columns(cols)

        assert actual == expected

    @mark.skip("""TODO""")
    # pylint: disable=no-self-use,missing-function-docstring
    def test_supply_mappings_for_duplicate_column_names(self) -> None:
        pass
