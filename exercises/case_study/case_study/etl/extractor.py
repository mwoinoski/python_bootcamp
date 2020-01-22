"""
Extractor class implementation.
"""

from typing import ClassVar, Dict, Any
from etl_logger import EtlLogger

from pyspark.sql import DataFrame, SparkSession


class ExtractorCsv:
    """ Extractor implements the "extract" process of ETL """
    input_schema: ClassVar[str] = \
        '`Customer ID` integer, `Order ID` integer, `Order Total` double'
    path: str
    logger: EtlLogger

    def __init__(self, config: Dict[str, Any]):
        self.path = config['path']
        self.logger = EtlLogger()

    def extract(self, spark: SparkSession) -> DataFrame:
        self.logger.info(f'Extract: {self.path}')

        df: DataFrame = spark.read.csv(self.path, header=True,
                                       schema=ExtractorCsv.input_schema)
        return df
