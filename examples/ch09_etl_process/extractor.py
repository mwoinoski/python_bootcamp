"""
Extractor class implementation.
"""

from typing import ClassVar
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession


class Extractor:
    """ Extractor implements the "extract" process of ETL """
    input_schema: ClassVar[str] = \
        '`Customer ID` integer, `Order ID` integer, `Order Total` double'

    def __init__(self):
        pass

    def extract(self, spark: SparkSession) -> DataFrame:
        file = 'customer-orders.csv'
        path = f'file://{Path().absolute()}/{file}'

        df: DataFrame = spark.read.csv(path, header=True,
                                       schema=Extractor.input_schema)
        return df
