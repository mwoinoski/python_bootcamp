"""
Unit test cases for Person class
"""

from unittest import TestCase
from people.person import Person


class PersonTest(TestCase):
    def test_init_all_values_(self):
        p = Person("Vivien", "Theodore", "Thomas")

        self.assertEqual("Vivien", p.given)
        self.assertEqual("Theodore", p.middle)
        self.assertEqual("Thomas", p.family)

    def test_init_given_family_only(self):
        p = Person("Elizabeth", None, "Blackwell")

        self.assertEqual("Elizabeth", p.given)
        self.assertIsNone(p.middle)
        self.assertEqual("Blackwell", p.family)

    def test_init_given_only(self):
        p = Person("Hippocrates", None, None)

        self.assertEqual("Hippocrates", p.given)
        self.assertIsNone(p.middle)
        self.assertIsNone(p.family)


if __name__ == "__main__":
    TestCase.main()
