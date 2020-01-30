"""
Extractor class implementation for extracting a database table.
"""

from typing import ClassVar, Dict, Any

from pyspark.sql import DataFrame, SparkSession

from case_study.etl.etl_logger import EtlLogger


class ExtractorDb:
    """ Extractor implements the "extract" process of ETL """
    # TODO: there's a lot of duplication in LoaderDb and ExtractDb, so
    #       extract a common superclass, e.g. DbEtlComponent
    # This is also a good use case for multiple inheritance:
    # ExtractorDb IS-A DbEtlComponent and ExtractorDb IS-A Loader
    # (but multiple inheritance can be tricky, so it might not be worth it)

    # input_schema: ClassVar[str] = ""
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
        """ Initialize the Extractor """
        self.db_driver = config.get('db_driver', ExtractorDb.default_db_driver)
        self.db_url = config.get('db_url', ExtractorDb.default_db_url)
        self.database_name = config['database_name']
        self.table_name = config['table_name']
        self.user = config['user']
        self.password = config['password']
        self.logger = EtlLogger()

    def extract(self, spark: SparkSession) -> DataFrame:
        """ Extract a DataFrame from a database query """
        self.logger.debug(f'Extract: {self.database_name}.{self.table_name}')
        try:
            # Extract a DataFrame from a SQLServer table
            input_df: DataFrame = spark.read.format('jdbc') \
                .option('driver', self.db_driver) \
                .option('url', self.db_url) \
                .option('dbtable', self.table_name) \
                .option('databaseName', self.database_name) \
                .option('user', self.user) \
                .option('password', self.password) \
                .load()

            self.logger.debug(
                f'Read {input_df.count()} records from {self.table_name}')
            return input_df
        except Exception as ex:
            self.logger.error(
                f'error while extracting {self.database_name}.{self.table_name}')
            raise
