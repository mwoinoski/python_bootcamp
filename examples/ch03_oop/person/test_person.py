"""
Unit tests for the Person class.
"""

from person.person import Person


def test_init_all_args_given() -> None:
    person: Person = Person("Curie", "Marie", "Skłodowska")

    assert person.given_name == "Marie"
    assert person.middle_name == "Skłodowska"
    assert person.family_name == "Curie"


def test_full_name_all_attributes_set() -> None:
    person: Person = Person("Curie", "Marie", "Skłodowska")

    result = person.full_name()

    assert result == "Marie Skłodowska Curie"


def test_full_name_empty_middle() -> None:
    person: Person = Person("Curie", "Marie", "")

    result = person.full_name()

    assert result == "Marie Curie"


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


def test_repr() -> None:
    patient: Person = Person("Curie", "Marie", "Skłodowska")

    expected: str = f"given_name='Marie',middle_name='Skłodowska',family_name='Curie'"
    assert repr(patient) == expected
