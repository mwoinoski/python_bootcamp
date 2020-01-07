"""
DAO for Persons
"""
from abc import ABCMeta, abstractmethod

from manage_accounts.model.person import Person
from manage_accounts.persistence.person_dao_lookup import PersonDaoLookup


class PersonDao(PersonDaoLookup, metaclass=ABCMeta):
    @abstractmethod
    def insert(self, person: Person) -> None:
        """ Insert a new Person object into the persistent collection """
        pass
