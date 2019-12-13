"""
Person class definition.
"""
from typing import Optional
from datetime import datetime


class Person:
    """
    Person encapsulates the common attributes of all persons in our application.
    """

    def __init__(self,
                 given: Optional[str] = None,
                 middle: Optional[str] = None,
                 family: Optional[str] = None,
                 person_id: Optional[int] = None) -> None:
        """ Initialize a Person """
        if not (given or middle or family):
            raise ValueError("all name arguments are empty or None")

        self.id: Optional[int] = person_id
        self.created_time: datetime = datetime.utcnow()
        # For names, replace None with an empty string
        self.given: str = given if given else ""
        self.middle: str = middle if middle else ""
        self.family: str = family if family else ""

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
            other.family == self.family

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
