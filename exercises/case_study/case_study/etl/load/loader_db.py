"""
Loader class implementation for loading a database table.
"""

from typing import ClassVar, List, Dict, Any
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession

from case_study.etl.etl_logger import EtlLogger


class LoaderDb:
    """ Loader implements the "load" process of ETL """

    default_db_driver: ClassVar[str] = 'com.microsoft.sqlserver.jdbc.SQLServerDriver'
    default_db_url: ClassVar[str] = 'jdbc:sqlserver://localhost'
    db_driver: str
    db_url: str
    database_name: str
    table_name: str
    user: str
    password: str
    logger: EtlLogger

    def __init__(self, config: Dict[str, Any]):
        """ Initialize the Loader """
        self.db_driver = config.get('db_driver', LoaderDb.default_db_driver)
        self.db_url = config.get('db_url', LoaderDb.default_db_url)
        self.database_name = config['database_name']
        self.table_name = config['table_name']
        self.user = config['user']
        self.password = config['password']
        self.logger = EtlLogger()

    def load(self, spark: SparkSession, df: DataFrame):
        """ Load the DataFrame to a database table file """
        self.logger.debug(f'Load: {self.database_name}.{self.table_name}')
        try:
            # Extract a DataFrame from a SQLServer table
            input_df: DataFrame = spark.write.format('jdbc') \
                .option('driver', self.db_driver) \
                .option('url', self.db_url) \
                .option('dbtable', self.table_name) \
                .option('databaseName', self.database_name) \
                .option('user', self.user) \
                .option('password', self.password) \
                .mode('overwrite') \
                .save()
            # default mode is 'create', which raises error if table exists
            # df.mode('append')  # add data to existing table
            # df.mode('overwrite')  # overwrite existing data

            self.logger.debug(
                f'Wrote {input_df.count()} records to {self.table_name}')
            return input_df
        except Exception as ex:
            self.logger.error(
                f'error while loading {self.database_name}.{self.table_name}')
            raise
