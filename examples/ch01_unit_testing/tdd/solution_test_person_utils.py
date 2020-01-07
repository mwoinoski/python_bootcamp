"""
Unit tests for person_utils.py
"""
from pytest import fail, mark

from solution_person_utils import get_full_name


def test_get_full_name_all_components_given():
    result = get_full_name("Curie", "Marie", "Skłodowska")

    assert result == "Marie Skłodowska Curie"


def test_full_name_empty_middle():
    result = get_full_name("Curie", "Marie", "")

    assert result == "Marie Curie"


def test_full_name_none_middle():
    result = get_full_name("Curie", "Marie", None)

    assert result == "Marie Curie"


def test_full_name_family_only():
    result = get_full_name("Einstein", None, None)

    assert result == "Einstein"


def test_full_name_given_only():
    result = get_full_name(None, "Aristotle", None)

    assert result == "Aristotle"


def test_full_name_middle_only():
    result = get_full_name(None, None, "Skłodowska")

    assert result == "Skłodowska"


@mark.skip('TODO: raise ValueError if all arguments are empty or None')
def test_init_all_args_empty():
    try:
        get_full_name("", "", "")
        fail('get_full_name("", "", "") should raise ValueError', pytrace=False)
    except ValueError:
        pass
