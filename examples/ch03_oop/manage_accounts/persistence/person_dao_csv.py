"""
CSV implementation of DAO for Persons
"""
from collections.abc import Iterable
from typing import ClassVar, Optional, List

from manage_accounts.model.person import Person
from manage_accounts.persistence.person_dao_lookup import PersonDao


class PersonDaoCsv(PersonDao):
    records: List[str]
    debug: bool

    def __init__(self, csv_filepath: str, debug: bool = False):
        """" Initialize DAO from a file """
        self.debug = debug
        # TODO:

    def find(self,
             given: Optional[str] = None,
             middle: Optional[str] = None,
             family: Optional[str] = None) -> Iterable:
        """ Look up Persons by name """
        if not (given or middle or family):
            raise ValueError("all arguments are empty or None")

        # TODO
        records = []

        for row in records:
            yield PersonDaoCsv.populate_person(row)

    def find_by_id(self, person_id: int) -> Optional[Person]:
        """ Look up a Person by ID """
        result: List[List[str]] = []  # TODO
        person: Optional[Person] = None
        if len(result) > 1:
            raise ValueError("duplicate id {person_id}")
        if len(result) > 0:
            person = PersonDaoCsv.populate_person(result.pop())
        return person

    def insert(self, person: Person) -> None:
        """ Insert a new Person object into the persistent collection """
        pass  # TODO

    def close(self) -> None:
        """ Write the CSV file """
        pass  # TODO

    @staticmethod
    def populate_person(row: List[str]) -> Person:
        """ Populate a Person from a Row """
        person = Person()
        return person
