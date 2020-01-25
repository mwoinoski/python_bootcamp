"""
Defines class for ETL processing
"""

from typing import Union, Any
from unittest.mock import Mock

from pyspark.sql import SparkSession, DataFrame

from case_study.etl.etl_logger import EtlLogger


def create_spark_session() -> SparkSession:
    """ Create a SparkSession """
    return SparkSession.builder \
                       .appName('ETL Process') \
                       .enableHiveSupport() \
                       .getOrCreate()


class EtlProcess:
    """ EtlProcess orchestrates the ETL process """

    spark: SparkSession
    extractor: Any  # better: create abstract base class Extractor
    transformer: Any
    loader: Any
    logger: EtlLogger

    def __init__(self, extractor, transformer, loader,
                 spark: Union[SparkSession, Mock] = create_spark_session()) \
            -> None:
        """ Initialize the EtlProcess """
        self.logger = EtlLogger()

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
        except Exception as ex:
            self.logger.error(f'ETL Process error: {ex}')
            raise ex
        finally:
            self.spark.stop()


class EtlProcessError(Exception):
    """ Exception class for ETL processing errors"""
    pass
