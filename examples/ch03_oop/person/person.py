"""
Person class definition.
"""

from typing import Optional


class Person:
    """
    Person encapsulates the common attributes of all persons in our application.
    """
    family_name: Optional[str]
    given_name: Optional[str]
    middle_name: Optional[str]

    def __init__(self, family: str, given: str, middle: str) -> None:
        """ Initialize a Person """
        self.family_name = family
        self.given_name = given
        self.middle_name = middle

    def full_name(self) -> str:
        """ Concatenate all name attributes with no additional spaces """
        names = [self.given_name, self.middle_name, self.family_name]
        return " ".join(n for n in names if n)

    def __eq__(self, other):
        """ Called when Person instances are compared with == operator """
        return isinstance(other, Person) and \
            other.given_name == self.given_name and \
            other.middle_name == self.middle_name and \
            other.family_name == self.family_name

    def __str__(self):
        """ Result is useful for to a client (e.g., in a report) """
        return self.full_name()

    def __repr__(self):
        """ Result is useful for a developer (e.g., in a debugger) """
        return f"given_name='{self.given_name}'," \
            f"middle_name='{self.middle_name}'," \
            f"family_name='{self.family_name}'"
