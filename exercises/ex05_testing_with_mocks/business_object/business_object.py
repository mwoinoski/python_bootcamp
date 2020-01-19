"""
business_object.py - Classes for exercising mock objects
"""

import sqlite3


class UserDao(object):
    """Class that encapsulates database access"""
    def __init__(self) -> None:
        pass  # Production DAO would create connection to database

    def query_user(self, user_id: int) -> Person:
        return Person(123, 'Isaac', None, 'Newton')
        # Production DAO would query database for user by ID


class BusinessObject:
    """Simple class for mock demo"""
    name: str
    user_dao: UserDao

    def __init__(self, name: str):
        self.name = name
        self.user_dao = UserDao()

    def get_user(self, user_id: int):
        if user_id is None or user_id < 1:
            raise ValueError(f'invalid user ID "{user_id}"')
        try:
            user: Person = self.user_dao.query_user(user_id)
            if user is None:
                raise ValueError(f'{user_id} is not a valid user ID')

            return user
        except sqlite3.Error as e:
            raise BusinessError(f'Problem fetching user with ID {user_id}: {e}')

    def __str__(self):
        return f"{self.name}"


class BusinessError(Exception):
    """Application-specific exception class"""
    def __init__(self, msg: str):
        super().__init__(msg)


class Person:
    """Simple class for testing mock objects"""
    id: int
    first_name: str
    middle_name: str
    last_name: str

    def __init__(self, user_id: int, first_name: str, middle_name: str, last_name: str):
        self.id = user_id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name

    def __eq__(self, other):
        """Called when Person instances are compared with == operator"""
        return isinstance(other, Person) and \
            other.first_name == self.first_name and \
            other.middle_name == self.middle_name and \
            other.last_name == self.last_name

    def __str__(self):
        return f"{self.id} {self.first_name} {self.middle_name} {self.last_name}"
