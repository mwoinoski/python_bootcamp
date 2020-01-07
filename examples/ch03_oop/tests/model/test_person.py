"""
Unit tests for the Person class.
"""

import copy
from manage_accounts.model.person import Person
from datetime import datetime
from pytest import raises


def test_init_middle_name_arg_is_none() -> None:
    person: Person = Person("Curie", "Marie", None)

    assert person.given_name == "Marie"
    assert person.middle_name == ""
    assert person.family_name == "Curie"


def test_full_name() -> None:
    person: Person = Person("Curie", "Marie", "Skłodowska")

    assert person.full_name() == "Marie Skłodowska Curie"


def test_full_name_empty_middle() -> None:
    person: Person = Person("Curie", "Marie", "")

    assert person.full_name() == "Marie Curie"


def test_full_name_null_middle() -> None:
    person: Person = Person("Curie", "Marie", None)

    assert person.full_name() == "Marie Curie"


def test_full_name_last_only() -> None:
    person: Person = Person("Einstein", None, None)

    assert person.full_name() == "Einstein"


def test_full_name_first_only() -> None:
    person: Person = Person(None, "Aristotle", None)

    assert person.full_name() == "Aristotle"


def test_full_name_middle_only() -> None:
    person: Person = Person(None, None, "Skłodowska")

    assert person.full_name() == "Skłodowska"


def test_init_all_args_empty() -> None:
    with raises(ValueError, match=r"[Aa]rg.*[Ee]mpty"):
        Person("", "", "")


def test_eq_instances_are_exact_copies() -> None:
    p1: Person = Person("Curie", "Marie", "Skłodowska")
    p2: Person = copy.deepcopy(p1)

    assert p1 == p2  # "==" calls p1.__eq__(p2) == p1


def test_eq_instances_equal() -> None:
    p1: Person = Person("Curie", "Marie", "Skłodowska")
    p2: Person = Person("Curie", "Marie", "Skłodowska")

    assert p1 != p2  # created_time attributes are (almost certainly) different


def test_eq_instances_not_equal() -> None:
    p1: Person = Person("Curie", "Marie", None)
    p2: Person = Person("Curie", "Marie", "Skłodowska")

    assert p1 != p2  # "!=" calls p1.__ne__(p2)


def test_str() -> None:
    person: Person = Person("Curie", "Marie", "Skłodowska")

    assert str(person) == "Marie Skłodowska Curie"


def test_repr() -> None:
    timestamp: str = "2019-11-14T14:31:39.629853"
    person: Person = Person(1, "Curie", "Marie", "Skłodowska", datetime.fromisoformat(timestamp))

    expected: str = f"id='1',given='Marie',middle='Skłodowska'," \
                    f"family='Curie',created_time='{timestamp}'"
    assert repr(person) == expected


def test_created_time() -> None:
    person: Person = Person("Curie", "Marie", "Skłodowska")

    assert person.created_time <= datetime.utcnow()
