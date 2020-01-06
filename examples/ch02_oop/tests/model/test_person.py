"""
Unit tests for the Person class.
"""

import copy
from manage_accounts.model.person import Person
from datetime import datetime
from pytest import raises


def test_init() -> None:
    person = Person("Marie", None, "Curie")

    assert "Marie" == person.given
    assert "" == person.middle
    assert "Curie" == person.family


def test_full_name() -> None:
    person = Person("Marie", "Skłodowska", "Curie")

    assert "Marie Skłodowska Curie" == person.full_name()


def test_full_name_empty_middle() -> None:
    person = Person("Marie", "", "Curie")

    assert "Marie Curie" == person.full_name()


def test_full_name_null_middle() -> None:
    person = Person("Marie", None, "Curie")

    assert "Marie Curie" == person.full_name()


def test_full_name_last_only() -> None:
    person = Person(None, None, "Einstein")

    assert "Einstein" == person.full_name()


def test_full_name_first_only() -> None:
    person = Person("Aristotle", None, None)

    assert "Aristotle" == person.full_name()


def test_full_name_middle_only() -> None:
    person = Person(None, "Skłodowska", None)

    assert "Skłodowska" == person.full_name()


def test_init_all_args_empty() -> None:
    with raises(ValueError, match=r"[Aa]rg.*[Ee]mpty"):
        Person("", "", "")


def test_eq_instances_are_exact_copies() -> None:
    p1 = Person("Marie", "Skłodowska", "Curie")
    p2 = copy.deepcopy(p1)

    assert p1 == p2  # "==" calls p1.__eq__(p2)


def test_eq_instances_equal() -> None:
    p1 = Person("Marie", "Skłodowska", "Curie")
    p2 = Person("Marie", "Skłodowska", "Curie")

    assert p1 != p2  # created_time attributes are (almost certainly) different


def test_eq_instances_not_equal() -> None:
    p1 = Person("Marie", None, "Curie")
    p2 = Person("Marie", "Skłodowska", "Curie")

    assert p1 != p2  # "!=" calls p1.__ne__(p2)


def test_str() -> None:
    person = Person("Marie", "Skłodowska", "Curie")

    assert "Marie Skłodowska Curie" == str(person)


def test_repr() -> None:
    timestamp = "2019-11-14T14:31:39.629853"
    person = Person("Marie", "Skłodowska", "Curie", 1,
                    datetime.fromisoformat(timestamp))

    expected = f"id='1',given='Marie',middle='Skłodowska'," \
               f"family='Curie',created_time='{timestamp}'"
    assert expected == repr(person)


def test_created_time() -> None:
    person = Person("Marie", "Skłodowska", "Curie")
    assert person.created_time <= datetime.utcnow()
