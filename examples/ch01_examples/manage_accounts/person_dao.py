"""
DAO for Persons
"""
from collections import Iterable
from typing import Optional
from abc import ABCMeta, abstractmethod

from manage_accounts.person import Person
from manage_accounts.person_dao_readonly import PersonDaoReadonly


class PersonDao(PersonDaoReadonly, metaclass=ABCMeta):
    @abstractmethod
    def insert(self, person: Person) -> None:
        """ Insert a new Person object into the persistent collection """
        pass
