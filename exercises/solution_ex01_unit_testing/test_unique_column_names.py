"""
Test cases for data_normalization.make_column_names_unique function
"""

from data_normalization import normalize_column_name, make_column_names_unique

# TODO: open data_normalization.py and read the requirements for the
# normalize_column_name function. Write unit tests that verify the code for the
# function meets the requirements.
# HINT: start with the simple cases:
#       1. call the function with argument None
#       2. call the function with argument ''
#       3. then write at least one test for each of the other requirements
# Try to think of as many "edge" conditions as possible. For example, for
# the max length requirement, try at least 3 separate tests:
# 1. a name with length (max - 1)
# 2. a name with length max
# 3. a name with length (max + 1)

def test_normalize_column_name_arg_is_none() -> None:
    # Arrange
    old_name = None
    # Act
    results = normalize_column_name(old_name)
    # Assert
    assert results == ""


def test_normalize_column_name_arg_is_empty() -> None:
    old_name = ""
    results = normalize_column_name(old_name)
    assert results == ""


def test_normalize_column_name_no_change() -> None:
    old_name = 'street'
    results = normalize_column_name(old_name)
    assert results == 'street'


def test_normalize_column_name_all_caps() -> None:
    old_name = 'STREET'
    results = normalize_column_name(old_name)
    assert results == 'street'


def test_normalize_column_name_internal_space() -> None:
    old_name = 'Street Address'
    results = normalize_column_name(old_name)
    assert results == 'street_address'


def test_normalize_column_name_leading_and_trailing_space() -> None:
    old_name = '    Street  Address   '
    results = normalize_column_name(old_name)
    assert results == 'street_address'


def test_normalize_column_name_special_chars() -> None:
    old_name = 'State/Province (req)'
    results = normalize_column_name(old_name)
    assert results == 'state_province_req'


def test_normalize_column_name_trailing_underscore() -> None:
    old_name = 'STATE_'
    results = normalize_column_name(old_name)
    assert results == 'state'


def test_normalize_column_name_length_max_minus_one() -> None:
    old_name = 'zip code'
    results = normalize_column_name(old_name, 9)
    assert results == 'zip_code'


def test_normalize_column_name_length_max() -> None:
    old_name = 'zip code'
    results = normalize_column_name(old_name, 8)
    assert results == 'zip_code'


def test_normalize_column_name_length_max_plus_one() -> None:
    old_name = 'zip code'
    results = normalize_column_name(old_name, 7)
    assert results == 'zip_cod'


def test_normalize_column_name_trailing_underscore_after_normalizing() -> None:
    old_name = 'zip code'
    results = normalize_column_name(old_name, 4)
    assert results == 'zip'


# TODO: open data_normalization.py and read the requirements for the
# make_column_names_unique function. Write unit tests that verify the code for
# the function meets the requirements.
# HINT: again, start with the simple cases:
#       1. call the function with argument None
#       2. call the function with an empty list
#       3. call the function with a list with one name that already meets the
#          requirements
#       3. then write at least one test for each of the other requirements

def test_make_column_names_unique_empty_list() -> None:
    old_cols = []
    results = make_column_names_unique(old_cols)
    assert results == []


def test_make_column_names_unique_one_column_no_change() -> None:
    old_cols = ['street']
    results = make_column_names_unique(old_cols)
    assert results == ['street']


def test_make_column_names_unique_one_column_all_caps() -> None:
    old_cols = ['STREET']
    results = make_column_names_unique(old_cols)
    assert results == ['street']


def test_make_column_names_unique_different_columns() -> None:
    old_cols = ['Street', 'City', 'ZIP Code']
    results = make_column_names_unique(old_cols)
    assert results == ['street', 'city', 'zip_code']


def test_make_column_names_unique_duplicate_names_before_normalizing() -> None:
    old_cols = ['Street', 'City', 'Street']
    results = make_column_names_unique(old_cols)
    assert results == ['street_1', 'city', 'street_2']


def test_make_column_names_unique_duplicate_names_after_normalizing() -> None:
    old_cols = ['Street', 'Zip_Code', 'State', 'ZIP Code']
    results = make_column_names_unique(old_cols)
    assert results == ['street', 'zip_code_1', 'state', 'zip_code_2']


def test_make_column_names_unique_duplicate_names_after_normalizing() -> None:
    old_cols = ['Street', 'Zip_Code', 'State', 'ZIP Code']
    results = make_column_names_unique(old_cols)
    assert results == ['street', 'zip_code_1', 'state', 'zip_code_2']


def test_make_column_names_unique_duplicate_names_after_normalizing() -> None:
    old_cols = ['Street', 'Zip_Code', 'State', 'ZIP Code']
    results = make_column_names_unique(old_cols)
    assert results == ['street', 'zip_code_1', 'state', 'zip_code_2']


def test_make_column_names_unique_duplicate_names_after_shortening() -> None:
    old_cols = ['Performance Score Mean', 'Performance Score Std Dev']
    results = make_column_names_unique(old_cols, 18)
    assert results == ['performance_scor_1', 'performance_scor_2']


def test_make_column_names_unique_ten_dupes() -> None:
    old_cols = ['name'] * 10
    results = make_column_names_unique(old_cols, 18)
    assert results == ['name_01', 'name_02', 'name_03', 'name_04', 'name_05',
                       'name_06', 'name_07', 'name_08', 'name_09', 'name_10']


def test_make_column_names_unique_ten_dupes() -> None:
    old_cols = ['name'] * 10
    results = make_column_names_unique(old_cols, 6)
    assert results == ['nam_01', 'nam_02', 'nam_03', 'nam_04', 'nam_05',
                       'nam_06', 'nam_07', 'nam_08', 'nam_09', 'nam_10']
