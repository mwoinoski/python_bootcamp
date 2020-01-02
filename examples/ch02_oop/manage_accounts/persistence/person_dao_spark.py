"""
Spark implementation of DAO for Persons
"""
from collections.abc import Iterable
from typing import ClassVar, Optional, List

from pyspark.sql import SparkSession, DataFrame, Row

from manage_accounts.model.person import Person
from manage_accounts.persistence.person_dao_readonly import PersonDaoReadonly

default_data_file_path: str = "file:///person_mgmt/person_dao_spark_test.jsonl"


class PersonDaoSpark(PersonDaoReadonly):
    schema: ClassVar[str] = """
        id int, given string, middle string, family string, created_time timestamp
    """
    df: DataFrame
    spark: SparkSession
    debug: bool

    def __init__(self,
                 data_path: str = default_data_file_path,
                 data_format: str = "json",
                 debug: bool = False):
        """" Initialize PySpark from a data file """
        self.debug = debug

        self.spark = SparkSession.builder \
            .appName("PersonDaoSpark") \
            .getOrCreate()
        self.df = self.spark.read.load(data_path, format=data_format,
                                       schema=PersonDaoSpark.schema)
        self.df.createOrReplaceTempView("person")

    def find(self,
             given: Optional[str] = None,
             middle: Optional[str] = None,
             family: Optional[str] = None) -> Iterable:
        """ Look up Persons by name """
        if not (given or middle or family):
            raise ValueError("all arguments are empty or None")

        query_df: DataFrame = self.df
        if given is not None:
            query_df = query_df.filter(query_df.given == given)
        if middle is not None:
            query_df = query_df.filter(query_df.middle == middle)
        if family is not None:
            query_df = query_df.filter(query_df.family == family)

        if self.debug:
            query_df.show()

        for row in query_df.collect():
            yield PersonDaoSpark.populate_person(row)

    def find_by_id(self, pid: int) -> Optional[Person]:
        """ Look up a Person by ID """
        result: List[Row] = self.df.filter(self.df.id == pid).collect()
        person: Optional[Person] = None
        if len(result) > 1:
            raise ValueError("duplicate id {pid}")
        if len(result) > 0:
            person = PersonDaoSpark.populate_person(result.pop())
        return person

    def close(self) -> None:
        """ Stop the SparkSession """
        self.spark.stop()

    @staticmethod
    def populate_person(row: Row) -> Person:
        """ Populate a Person from a Row """
        person = Person(row["given"], row["middle"], row["family"])
        person.id = row["id"]
        person.created_time = row["created_time"]
        return person
