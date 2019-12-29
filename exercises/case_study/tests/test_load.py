"""
Test the results of the ETL process.
"""

from configparser import ConfigParser
from typing import Dict, ClassVar
from unittest import TestCase

from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as f


class LoadTest(TestCase):
    """ LoadTest defines integration tests of the results of the ETL process """
    spark: ClassVar[SparkSession]
    db_config: ClassVar[Dict[str, str]]

    @classmethod
    def setup_class(cls):
        """ Load a Spark DataFrame from a DB table """

        config: ConfigParser = ConfigParser()
        config_file = 'test_config.ini'
        if not config.read(config_file):
            raise Exception(f"couldn't read config file {config_file}")

        cls.db_config: Dict[str, str] = config['load']

        # initialize spark
        cls.spark = SparkSession.builder \
                                .appName('ETL Integration Test') \
                                .getOrCreate()

    @classmethod
    def load_dataframe(cls, table_name: str) -> DataFrame:
        """ Loads a DataFrame from a database table """
        return LoadTest.spark.read \
            .format(cls.db_config['format']) \
            .option('url', cls.db_config['url']) \
            .option('dbtable', table_name) \
            .option('driver', cls.db_config['driver']) \
            .option('user', cls.db_config['user']) \
            .option('password', cls.db_config['password']) \
            .load()

    # pylint: disable=no-self-use,missing-function-docstring
    def test_load_success(self):
        df: DataFrame = LoadTest.load_dataframe('esrd_qip_clean')

        assert df.count() == 6485
