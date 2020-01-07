"""
Person class definition.
"""
from typing import Optional
from datetime import datetime

from manage_accounts.model.address import Address


class Person:
    """
    Person encapsulates the common attributes of all persons in our application.
    """
    id: Optional[int]
    family_name: Optional[str]
    given_name: Optional[str]
    middle_name: Optional[str]
    created_time: Optional[datetime]
    home_address: Optional[Address]
    work_address: Optional[Address]

    def __init__(self,
                 database_id: Optional[int] = None,
                 family: Optional[str] = None,
                 given: Optional[str] = None,
                 middle: Optional[str] = None,
                 timestamp: Optional[datetime] = None) -> None:
        """ Initialize a Person """
        if not (given or middle or family):
            raise ValueError("all name arguments are empty or None")

        # For names, replace None with an empty string
        self.given_name = given if given else ""
        self.middle_name = middle if middle else ""
        self.family_name = family if family else ""

        self.id = database_id
        self.created_time = timestamp if timestamp else datetime.utcnow()
        self.home_address = None
        self.work_address = None

    def full_name(self) -> str:
        """ Concatenate all name attributes with no additional spaces """
        names = [self.given_name, self.middle_name, self.family_name]
        return " ".join(n for n in names if n)

    def __eq__(self, other):
        """ Called when Person instances are compared with == operator """
        return isinstance(other, Person) and \
            other.id == self.id and \
            other.given_name == self.given_name and \
            other.middle_name == self.middle_name and \
            other.family_name == self.family_name and \
            other.created_time == self.created_time and \
            other.home_address == self.home_address and \
            other.work_address == self.work_address

    def __str__(self):
        """ Result is useful for a client """
        return self.full_name()

    def __repr__(self):
        """ Result is useful for a developer (for example, in a debugger) """
        return f"id='{self.id}'," \
            f"given='{self.given_name}'," \
            f"middle='{self.middle_name}'," \
            f"family='{self.family_name}'," \
            f"created_time='{self.created_time.isoformat()}'"
