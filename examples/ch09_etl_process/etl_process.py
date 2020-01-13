"""
Defines class for ETL processing
"""
from typing import Union
from unittest.mock import Mock
import logging.config

from pyspark.sql import SparkSession, DataFrame

from extractor import Extractor
from loader import Loader
from transformer import Transformer


def create_spark_session() -> SparkSession:
    """ Create a SparkSession """
    return SparkSession.builder \
                       .appName('ETL Process') \
                       .getOrCreate()


class EtlProcess:
    """ EtlProcess orchestrates the ETL process """

    extractor: Union[Extractor, Mock]
    transformer: Union[Transformer, Mock]
    loader: Union[Loader, Mock]

    logging_config_file: str = 'logging.ini'
    logger_name: str = 'etl_process'
    logger: logging.Logger

    def __init__(self,
                 spark: Union[SparkSession, Mock] = create_spark_session(),
                 extractor: Union[Extractor, Mock] = Extractor(),
                 transformer: Union[Transformer, Mock] = Transformer(),
                 loader: Union[Loader, Mock] = Loader()) -> None:
        """ Initialize the EtlProcess """
        logging.config.fileConfig(self.logging_config_file)
        self.logger = logging.getLogger(self.logger_name)

        # initialize Spark
        self.spark = spark
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self) -> None:
        """ Run the ETL process """
        self.logger.debug('starting run')
        try:
            initial_df: DataFrame = self.extractor.extract(self.spark)
            transformed_df: DataFrame = \
                self.transformer.transform(self.spark, initial_df)
            self.loader.load(self.spark, transformed_df)
        finally:
            self.spark.stop()


class EtlProcessError(Exception):
    """ Exception class for ETL processing errors"""
    pass


if __name__ == '__main__':
    etl_process = EtlProcess()
    etl_process.run()
    etl_process.logger.info('ETL process complete')
