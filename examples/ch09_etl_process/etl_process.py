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
            original_df: DataFrame = self.extract()
            transformed_df: DataFrame = self.transform(original_df)
            self.load(transformed_df)
        finally:
            self.spark.stop()

    def extract(self) -> DataFrame:
        """ Extract the data to be transformed """
        self.logger.debug('starting extract')
        return self.extractor.extract(self.spark)

    def transform(self, df: DataFrame) -> DataFrame:
        """ Apply the transformations to the extracted data """
        self.logger.debug('starting transform')
        return self.transformer.transform(self.spark, df)

    def load(self, df: DataFrame) -> None:
        """ Load the transformed data to the target """
        self.logger.debug('starting load')
        self.loader.load(self.spark, df)


class EtlProcessError(Exception):
    """ Exception class for ETL processing errors"""
    pass


if __name__ == '__main__':
    etl_process = EtlProcess()
    etl_process.run()
    etl_process.logger.info('ETL process complete')
