"""
DAO for Persons
"""
from collections import Iterable
from typing import Optional

from pymongo import MongoClient

from manage_accounts.person import Person


class PersonDao:
    def __init__(self):
        self.client = MongoClient()  # MongoClient('mongodb://localhost:27017/')
        self.db = self.client.accounts  # use accounts
        self.collection = self.db.person  # collection person

    def insert(self, person: Person):
        person._id = self.collection.insert_one(vars(person)).inserted_id

    def find(self, first: Optional[str] = None,
             middle: Optional[str] = None,
             last: Optional[str] = None) -> Iterable:
        """ Initialize a Person """
        if not (first or middle or last):
            raise ValueError("all arguments are empty or None")
        query = {}
        if first is not None:
            query["first_name"] = first
        if middle is not None:
            query["middle_name"] = middle
        if last is not None:
            query["last_name"] = last

        for p in self.collection.find(query):
            person = Person(p["first_name"], p["middle_name"], p["last_name"])
            person._id = p["_id"]
            person.created_time = p["created_time"]
            yield person
