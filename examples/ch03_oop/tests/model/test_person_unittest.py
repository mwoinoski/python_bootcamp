"""
Unit tests, implemented with the unittest module, for the Person class.
"""

import copy
from manage_accounts.model.person import Person
from datetime import datetime
import unittest


class PersonTest(unittest.TestCase):
    def test_init(self):
        person = Person("Curie", "Marie", None)
    
        self.assertEqual("Marie", person.given_name)
        self.assertEqual("", person.middle_name)
        self.assertEqual("Curie", person.family_name)

    def test_full_name(self):
        person = Person("Curie", "Marie", "Skłodowska")

        full_name = person.full_name()

        self.assertEqual("Marie Skłodowska Curie", full_name)

    def test_full_name_empty_middle(self):
        person = Person("Curie", "Marie", "")

        full_name = person.full_name()

        self.assertEqual("Marie Curie", full_name)

    def test_full_name_null_middle(self):
        person = Person("Curie", "Marie", None)

        full_name = person.full_name()

        self.assertEqual("Marie Curie", full_name)

    def test_full_name_last_only(self):
        person = Person("Einstein", None, None)

        full_name = person.full_name()

        self.assertEqual("Einstein", full_name)

    def test_full_name_first_only(self):
        person = Person(None, "Aristotle", None)

        full_name = person.full_name()

        self.assertEqual("Aristotle", full_name)

    def test_full_name_middle_only(self):
        person = Person(None, None, "Skłodowska")

        full_name = person.full_name()

        self.assertEqual("Skłodowska", full_name)

    def test_init_all_args_empty(self):
        with self.assertRaisesRegex(ValueError, r"[Aa]rg.*[Ee]mpty"):
            Person("", "", "")

    def test_eq_instances_are_exact_copies(self):
        p1 = Person("Curie", "Marie", "Skłodowska")
        p2 = copy.deepcopy(p1)
    
        self.assertTrue(p1 == p2)  # "==" calls p1.__eq__(p2))
    
    def test_eq_instances_equal(self):
        p1 = Person("Curie", "Marie", "Skłodowska")
        p2 = Person("Curie", "Marie", "Skłodowska")
    
        self.assertTrue(p1 != p2)  # created_time attributes are (almost certainly) different

    def test_eq_instances_not_equal(self):
        p1 = Person("Curie", "Marie", None)
        p2 = Person("Curie", "Marie", "Skłodowska")
    
        self.assertTrue(p1 != p2)  # "!=" calls p1.__ne__(p2)

    def test_str(self):
        person = Person("Curie", "Marie", "Skłodowska")

        person_str = str(person)

        self.assertEqual("Marie Skłodowska Curie", person_str)

    def test_repr(self):
        timestamp = "2019-11-14T14:31:39.629853"
        person = Person(1, "Curie", "Marie", "Skłodowska", datetime.fromisoformat(timestamp))
        expected = f"id='1',given='Marie',middle='Skłodowska'," \
                   f"family='Curie',created_time='{timestamp}'"

        person_repr = repr(person)

        self.assertEqual(expected, person_repr)

    def test_created_time(self):
        person = Person("Curie", "Marie", "Skłodowska")

        self.assertTrue(person.created_time <= datetime.utcnow())


if __name__ == '__main__':
    unittest.main()