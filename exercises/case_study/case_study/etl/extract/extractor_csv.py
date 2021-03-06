"""
Extractor class implementation.
"""

from typing import ClassVar, Dict, Any

from pyspark.sql import DataFrame, SparkSession

from case_study.etl.etl_logger import EtlLogger


class ExtractorCsv:
    """ Extractor implements the "extract" process of ETL """
    # input_schema: ClassVar[str] = ""
    path: str
    logger: EtlLogger

    def __init__(self, config: Dict[str, Any]):
        """ Initialize the Extractor """
        self.path = config['path']
        self.logger = EtlLogger()

    def extract(self, spark: SparkSession) -> DataFrame:
        """ Extract a DataFrame from a CSV file """
        self.logger.debug(f'Extract: {self.path}')
        try:
            df: DataFrame = spark.read.csv(self.path, header=True)
            self.logger.debug(f'read {df.count()} rows from {self.path}')
            return df
        except Exception as ex:
            self.logger.error(f'error while extracting {self.path}')
            raise
