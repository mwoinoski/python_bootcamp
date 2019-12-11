"""
Person class definition.
"""
from typing import Optional
from datetime import datetime


class Person:
    """
    Person encapsulates the common attributes of all persons in our application.
    """

    def __init__(self, first: Optional[str] = None,
                 middle: Optional[str] = None,
                 last: Optional[str] = None) -> None:
        """ Initialize a Person """
        if not (first or middle or last):
            raise ValueError("all arguments are empty or None")

        # Replace None with an empty string
        self.first_name: str = first if first else ""
        self.middle_name: str = middle if middle else ""
        self.last_name: str = last if last else ""
        self.created_time: datetime = datetime.utcnow()

    def full_name(self) -> str:
        """ Concatenate all name attributes with no additional spaces """
        names = [self.first_name, self.middle_name, self.last_name]
        return " ".join(n for n in names if n)

    def __eq__(self, other):
        """Called when Person instances are compared with == operator"""
        return isinstance(other, Person) and \
            other.first_name == self.first_name and \
            other.middle_name == self.middle_name and \
            other.last_name == self.last_name

    def __str__(self):
        """ Result is useful for a client """
        return self.full_name()

    def __repr__(self):
        """ Result is useful for a developer (for example, in a debugger) """
        return f"_id='{self._id}'," \
            f"first_name='{self.first_name}'," \
            f"middle_name='{self.middle_name}'," \
            f"last_name='{self.last_name}'," \
            f"created_time='{self.created_time.isoformat()}'"
