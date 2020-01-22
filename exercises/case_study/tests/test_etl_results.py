"""
Test the results of the ETL process. These tests assume the ETL process has
already completed.

To run the ETL process and then follow it with these tests, use the sheel script
run_integration_test.sh
"""

from configparser import ConfigParser
from typing import Dict, ClassVar
from unittest import TestCase

from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as f
from pytest import mark


class EtlProcessTest(TestCase):
    """ EtlProcessTest defines integration tests of the ETL process """

    config_file: ClassVar[str] = 'config-integration-test.ini'
    spark: ClassVar[SparkSession]
    db_config: ClassVar[Dict[str, str]]

    @classmethod
    def setup_class(cls):
        """ Initialize a SparkSession """

        config: ConfigParser = ConfigParser()
        if not config.read(cls.config_file):
            raise Exception(f"couldn't read config file {cls.config_file}")

        cls.db_config: Dict[str, str] = config['db']

        # initialize spark
        cls.spark = SparkSession.builder \
                                .appName('ETL Integration Test') \
                                .enableHiveSupport() \
                                .getOrCreate()

        cls.spark.sparkContext.setLocalProperty(
            "spark.sql.warehouse.dir", "/home/hive/warehouse")

    @classmethod
    def teardown_class(cls):
        """ Stop SparkSession """
        cls.spark.stop()

    @classmethod
    def load_from_database(cls, table_name: str) -> DataFrame:
        """ Loads a Spark DataFrame from a database table """
        return EtlProcessTest.spark.read \
            .format(cls.db_config['format']) \
            .option('url', cls.db_config['url']) \
            .option('dbtable', table_name) \
            .option('driver', cls.db_config['driver']) \
            .option('user', cls.db_config['user']) \
            .option('password', cls.db_config['password']) \
            .write_to_db()

    # pylint: disable=no-self-use,missing-function-docstring
    def test_load_success(self):
        df: DataFrame = EtlProcessTest.load_from_database('esrd_qip_clean')

        assert df.count() == 6549

    @mark.skip("need to get Hive set up")
    def test_hive_connection(self):
        query: str = """
            select * from pokes order by foo desc
        """
        hive_df: DataFrame = EtlProcessTest.spark.sql(query)
        hive_df.show(5)
        # print(hive_df.select(hive_df.foo == 1)[0])
        #
        # assert hive_df.count() == 500
        # assert hive_df.select(hive_df.foo == 1)[0]['bar'] == 'val_1'
