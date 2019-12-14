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
    given: Optional[str]
    middle: Optional[str]
    family: Optional[str]
    created_time: Optional[datetime]

    home_address: Address
    work_address: Optional[Address]

    def __init__(self,
                 given: Optional[str] = None,
                 middle: Optional[str] = None,
                 family: Optional[str] = None,
                 database_id: Optional[int] = None,
                 timestamp: Optional[datetime] = None) -> None:
        """ Initialize a Person """
        if not (given or middle or family):
            raise ValueError("all name arguments are empty or None")

        # For names, replace None with an empty string
        self.given = given if given else ""
        self.middle = middle if middle else ""
        self.family = family if family else ""

        self.id = database_id
        self.created_time = timestamp if timestamp else datetime.utcnow()

    def full_name(self) -> str:
        """ Concatenate all name attributes with no additional spaces """
        names = [self.given, self.middle, self.family]
        return " ".join(n for n in names if n)

    def __eq__(self, other):
        """ Called when Person instances are compared with == operator """
        return isinstance(other, Person) and \
            other.id == self.id and \
            other.given == self.given and \
            other.middle == self.middle and \
            other.family == self.family and \
            other.created_time == self.created_time

    def __str__(self):
        """ Result is useful for a client """
        return self.full_name()

    def __repr__(self):
        """ Result is useful for a developer (for example, in a debugger) """
        return f"id='{self.id}'," \
            f"given='{self.given}'," \
            f"middle='{self.middle}'," \
            f"family='{self.family}'," \
            f"created_time='{self.created_time.isoformat()}'"
