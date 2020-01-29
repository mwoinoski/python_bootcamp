"""
Drone class definition.
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

class Drone(Person):
    """
    Drone has a subset of Person attributes
    """

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self, given: str) -> None:
        """ Initialize a Drone """
        self.given_name = given
