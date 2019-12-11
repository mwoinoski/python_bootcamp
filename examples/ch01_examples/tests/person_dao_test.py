"""
Unit tests for PersonDao
"""
from datetime import datetime
from unittest import TestCase, main, skip

from bson import ObjectId
from pymongo import MongoClient

from manage_accounts.person import Person
from manage_accounts.person_dao import PersonDao
from pprint import pprint


class PersonDaoTest(TestCase):
    collection = None

    @classmethod
    def setUpClass(cls):
        client = MongoClient()  # MongoClient('mongodb://localhost:27017/')
        db = client.accounts  # use accounts
        PersonDao.collection = db.person

    def setUp(self):
        self.dao = PersonDao()

    @skip
    def test_insert(self):
        person = Person(None, None, None)
        self.dao.insert(person)
        self.assertIsNotNone(person._id)

    def test_find(self):
        results = [person for person in self.dao.find(
                    "Gottfried", "Wilhelm", "Leibniz")]
        self.assertEquals(1, len(results))
        p = results[0]
        self.assertIsInstance(p, Person)
        self.assertIsInstance(p._id, ObjectId)
        self.assertEqual(("Gottfried", "Wilhelm", "Leibniz"),
                          (p.first_name, p.middle_name, p.last_name))
        self.assertTrue(p.created_time < datetime.utcnow())


if __name__ == '__main__':
    main()
