"""
Unit tests for PersonDao
"""
from datetime import datetime
import os
from os.path import dirname, abspath, join
from tempfile import mkstemp
from typing import ClassVar, List, Optional, TextIO
from textwrap import dedent
from unittest import TestCase, main

from manage_accounts.model.person import Person
from manage_accounts.persistence.person_dao_spark import PersonDaoSpark
# from pprint import pprint  # pretty-print Python data structures


class PersonDaoSparkTest(TestCase):
    dao: PersonDaoSpark
    temp_file: Optional[TextIO]
    temp_file_handle: int
    temp_file_path: str
    data_file: ClassVar[str] = join(dirname(abspath(__file__)),
                                    "person_test.jsonl")

    def setUp(self) -> None:
        print(self.data_file)
        # create temp file
        self.temp_file_handle, self.temp_file_path = mkstemp(text=True)
        self.temp_file = open(self.temp_file_path, "w")

    def tearDown(self) -> None:
        if self.dao:
            self.dao.close()
        if self.temp_file:  # else file was closed in init_test_data()
            self.temp_file.close()
        if self.temp_file_handle:  # remove temp file
            os.close(self.temp_file_handle)
            os.remove(self.temp_file_path)

    def init_test_data(self, test_data: str) -> None:
        self.temp_file.write(dedent(test_data))
        self.temp_file.close()
        self.temp_file = None

    def test_find_all_parts(self) -> None:
        self.dao = PersonDaoSpark(PersonDaoSparkTest.data_file)
        # self.dao.df.printSchema()

        results = [person for person in self.dao.find(
                    "Vivien", "Theodore", "Thomas")]
        self.assertEqual(1, len(results))
        p = results[0]
        self.assertIsInstance(p, Person)
        self.assertEqual((1, "Vivien", "Theodore", "Thomas"),
                         (p.id, p.given, p.middle, p.family))
        self.assertTrue(p.created_time < datetime.utcnow())

    def test_find_given_only(self) -> None:
        self.dao = PersonDaoSpark(PersonDaoSparkTest.data_file)

        results = [person for person in self.dao.find("Elizabeth")]
        self.assertEqual(1, len(results))
        p = results[0]
        self.assertIsInstance(p, Person)
        self.assertEqual((2, "Elizabeth", "", "Blackwell"),
                         (p.id, p.given, p.middle, p.family))
        self.assertTrue(p.created_time < datetime.utcnow())

    def test_find_given_only_two_results(self) -> None:
        self.dao = PersonDaoSpark(PersonDaoSparkTest.data_file)

        results = [person for person in self.dao.find("Thomas")]
        self.assertEqual(2, len(results))
        sorted(results, key=lambda person: person.id)
        self.assertEqual(
            [(p.id, p.given, p.middle, p.family) for p in results],
            [(4, "Thomas", "", "Addison"), (5, "Thomas", "", "Sydenham")])

    def test_find_several_queries(self) -> None:
        self.dao = PersonDaoSpark(PersonDaoSparkTest.data_file)

        # next(iter(...)) performs one iteration of the Iterable argument
        p: Person = next(iter(self.dao.find("Vivien", "Theodore", "Thomas")))
        self.assertEqual(("Vivien", "Theodore", "Thomas"),
                          (p.given, p.middle, p.family))

        p = next(iter(self.dao.find("Elizabeth", family="Blackwell")))
        self.assertEqual(("Elizabeth", "", "Blackwell"),
                          (p.given, p.middle, p.family))

        p = next(iter(self.dao.find("Hippocrates")))
        self.assertEqual(("Hippocrates", "", ""),
                          (p.given, p.middle, p.family))

    def test_find_not_present(self) -> None:
        self.dao = PersonDaoSpark(PersonDaoSparkTest.data_file)

        results: List[Person] = [person for person in self.dao.find("NotThere")]
        self.assertEqual(0, len(results))

    def test_find_no_args(self) -> None:
        self.dao = PersonDaoSpark(PersonDaoSparkTest.data_file)

        with self.assertRaisesRegex(ValueError, r"arguments.*empty"):
            next(iter(self.dao.find()))
            # find() is s generator function, so it won't be executed unless
            # it's used for iteration

    def test_find_by_id_success(self) -> None:
        self.dao = PersonDaoSpark(PersonDaoSparkTest.data_file)

        person: Person = self.dao.find_by_id(3)
        self.assertEqual("Hippocrates", person.given)

    def test_find_by_id_not_present(self) -> None:
        self.dao = PersonDaoSpark(PersonDaoSparkTest.data_file)

        self.assertIsNone(self.dao.find_by_id(0))

    def test_find_by_id_json(self) -> None:
        self.init_test_data("""
            {"id": 1, "given": "Vivien", "middle": "Theodore", "family": "Thomas", "created_time": 1576109811}
            {"id": 2, "given": "Hippocrates", "created_time": 1576109813}
            {"id": 3, "given": "Thomas", "family": "Addison", "created_time": 1576109814}
            """)

        self.dao = PersonDaoSpark(self.temp_file_path)

        person: Person = self.dao.find_by_id(2)
        self.assertEqual("Hippocrates", person.given)

    def test_find_by_id_csv(self) -> None:
        self.init_test_data("""\
            1,Vivien,Theodore,Thomas,1576109811
            2,Hippocrates,,1576109812
            3,Thomas,,Addison,1576109813
            """)

        self.dao = PersonDaoSpark(self.temp_file_path, "csv")

        person: Person = self.dao.find_by_id(2)
        self.assertEqual("Hippocrates", person.given)

    def test_find_by_id_duplicate_id(self) -> None:
        self.init_test_data("""\
            {"id": 1, "given": "Vivien", "middle": "Theodore", "family": "Thomas", "created_time": 1576109811}
            {"id": 2, "given": "Hippocrates", "created_time": 1576109813}
            {"id": 2, "given": "Thomas", "family": "Addison", "created_time": 1576109814}
            """)

        self.dao = PersonDaoSpark(self.temp_file_path)

        with self.assertRaisesRegex(ValueError, r"duplicate.*([Ii][Dd]|[Kk]ey)"):
            self.dao.find_by_id(2)


if __name__ == '__main__':
    main()
