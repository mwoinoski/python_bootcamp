"""
MongoDB implementation of DAO for Persons
"""
from collections import Iterable
from typing import Optional

from pymongo import MongoClient

from manage_accounts.model.person import Person
from manage_accounts.persistence.person_dao import PersonDao


class PersonDaoMongoDb(PersonDao):
    def __init__(self):
        self.client = MongoClient()  # MongoClient('mongodb://localhost:27017/')
        self.db = self.client.accounts  # use accounts
        self.collection = self.db.person  # collection person

    def insert(self, person: Person):
        person._id = self.collection.insert_one(vars(person)).inserted_id

    def find(self, given: Optional[str] = None,
             middle: Optional[str] = None,
             family: Optional[str] = None) -> Iterable:
        """ Initialize a Person """
        if not (given or middle or family):
            raise ValueError("all arguments are empty or None")
        query = {}
        if given is not None:
            query["given"] = given
        if middle is not None:
            query["middle"] = middle
        if family is not None:
            query["family"] = family

        for p in self.collection.find(query):
            person = Person(p["given"], p["middle"], p["family"])
            person._id = p["_id"]
            person.created_time = p["created_time"]
            yield person

    def close(self) -> None:
        """ Disconnect from the MongoDb instance """
        self.client.close()