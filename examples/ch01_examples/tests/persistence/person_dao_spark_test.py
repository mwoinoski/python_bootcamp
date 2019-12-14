"""
Unit tests for PersonDao
"""
from datetime import datetime
import os
from os.path import dirname, abspath, join
from pytest import raises
from tempfile import mkstemp
from typing import List, Optional, TextIO
from textwrap import dedent

from manage_accounts.model.person import Person
from manage_accounts.persistence.person_dao_spark import PersonDaoSpark
# from pprint import pprint  # pretty-print Python data structures

dao: PersonDaoSpark
temp_file: Optional[TextIO]
temp_file_handle: int
temp_file_path: str
data_file_path: str = join(dirname(abspath(__file__)),
                           "person_dao_spark_test.jsonl")


def setup_function() -> None:
    # create temp file
    global temp_file_handle, temp_file_path, temp_file
    temp_file_handle, temp_file_path = mkstemp(text=True)
    temp_file = open(temp_file_path, "w")


def teardown_function() -> None:
    global dao, temp_file_handle, temp_file
    if dao:
        dao.close()
    if temp_file:  # else file was closed in init_test_data()
        temp_file.close()
    if temp_file_handle:  # remove temp file
        os.close(temp_file_handle)
        os.remove(temp_file_path)


def init_test_data(test_data: str) -> None:
    global temp_file
    temp_file.write(dedent(test_data))
    temp_file.close()
    temp_file = None


def test_find_all_args_supplied() -> None:
    global dao
    dao = PersonDaoSpark(data_file_path)
    # dao.df.printSchema()

    results = [person for person in dao.find(
                "Vivien", "Theodore", "Thomas")]
    assert 1 == len(results)
    p = results[0]
    assert isinstance(p, Person)
    assert (1, "Vivien", "Theodore", "Thomas") == \
           (p.id, p.given, p.middle, p.family)
    assert p.created_time < datetime.utcnow()


def test_find_given_arg_only() -> None:
    global dao
    dao = PersonDaoSpark(data_file_path)

    results = [person for person in dao.find("Elizabeth")]
    assert 1 == len(results)
    p = results[0]
    assert isinstance(p, Person)
    assert (2, "Elizabeth", "", "Blackwell") == \
           (p.id, p.given, p.middle, p.family)
    assert p.created_time < datetime.utcnow()


def test_find_given_arg_only_two_results() -> None:
    global dao
    dao = PersonDaoSpark(data_file_path)

    results = [person for person in dao.find("Thomas")]
    assert 2 == len(results)
    sorted(results, key=lambda person: person.id)
    assert [(p.id, p.given, p.middle, p.family) for p in results] == \
           [(4, "Thomas", "", "Addison"),
            (5, "Thomas", "", "Sydenham")]


def test_find_several_queries() -> None:
    global dao
    dao = PersonDaoSpark(data_file_path)

    # next(iter(...)) performs one iteration of the Iterable    argument
    p: Person = next(iter(dao.find("Vivien", "Theodore", "Thomas")))
    assert ("Vivien", "Theodore", "Thomas") == (p.given, p.middle, p.family)

    p = next(iter(dao.find("Elizabeth", family="Blackwell")))
    assert ("Elizabeth", "", "Blackwell") == (p.given, p.middle, p.family)

    p = next(iter(dao.find("Hippocrates")))
    assert ("Hippocrates", "", "") == (p.given, p.middle, p.family)


def test_find_person_not_present() -> None:
    global dao
    dao = PersonDaoSpark(data_file_path)

    results: List[Person] = [person for person in dao.find("NotThere")]
    assert 0 == len(results)


def test_find_no_args_raises_exception() -> None:
    global dao
    dao = PersonDaoSpark(data_file_path)

    with raises(ValueError, match=r"arguments.*empty"):
        next(iter(dao.find()))
        # find() is s generator function, so it won't be executed unless
        # it's used for iteration


def test_find_by_id_success() -> None:
    global dao
    dao = PersonDaoSpark(data_file_path)

    person: Person = dao.find_by_id(3)
    assert "Hippocrates" == person.given


def test_find_by_id_not_present() -> None:
    global dao
    dao = PersonDaoSpark(data_file_path)

    assert dao.find_by_id(0) is None


def test_find_by_id_json() -> None:
    global dao
    init_test_data("""
        {"id": 1, "given": "Vivien", "middle": "Theodore", "family": "Thomas", "created_time": 1576109811}
        {"id": 2, "given": "Hippocrates", "created_time": 1576109813}
        {"id": 3, "given": "Thomas", "family": "Addison", "created_time": 1576109814}
        """)

    dao = PersonDaoSpark(temp_file_path)

    person: Person = dao.find_by_id(2)
    assert "Hippocrates" == person.given


def test_find_by_id_csv() -> None:
    global dao
    init_test_data("""\
        1,Vivien,Theodore,Thomas,1576109811
        2,Hippocrates,,1576109812
        3,Thomas,,Addison,1576109813
        """)

    dao = PersonDaoSpark(temp_file_path, "csv")

    person: Person = dao.find_by_id(2)
    assert "Hippocrates" == person.given


def test_find_by_id_duplicate_id_raises_exception() -> None:
    global dao
    init_test_data("""\
        {"id": 1, "given": "Vivien", "middle": "Theodore", "family": "Thomas", "created_time": 1576109811}
        {"id": 2, "given": "Hippocrates", "created_time": 1576109813}
        {"id": 2, "given": "Thomas", "family": "Addison", "created_time": 1576109814}
        """)

    dao = PersonDaoSpark(temp_file_path)

    with raises(ValueError, match=r"duplicate.*([Ii][Dd]|[Kk]ey)"):
        dao.find_by_id(2)
