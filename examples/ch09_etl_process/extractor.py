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

    def extract(self, spark: SparkSession) -> DataFrame:
        file = 'customer-orders.csv'
        path = f'file://{Path().absolute()}/{file}'
        # path = f'hdfs://user/sutter/data/{file}'  # write to Hadoop HDFS

        df: DataFrame = spark.read.csv(path, header=True,
                                       schema=Extractor.input_schema)
        return df
