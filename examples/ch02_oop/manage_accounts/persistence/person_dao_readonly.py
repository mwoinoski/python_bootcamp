"""
DAO for Persons
"""
from collections import Iterable
from typing import Optional
from abc import ABCMeta, abstractmethod

from manage_accounts.model.person import Person


class PersonDaoReadonly(metaclass=ABCMeta):
    @abstractmethod
    def find(self,
             given: Optional[str] = None,
             middle: Optional[str] = None,
             family: Optional[str] = None) -> Iterable:
        """ Look up Persons by name """
        pass

    @abstractmethod
    def find_by_id(self, pid: int) -> Optional[Person]:
        """ Look up a Person by ID """
        pass

    @abstractmethod
    def close(self) -> None:
        """ Close the DAO """
        pass
