"""
Unit tests for Extractor
"""
from typing import ClassVar, Any, Dict
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession

from extractor import ExtractorCsv


class TestExtractor:
    spark: ClassVar[SparkSession]

    @classmethod
    def setup_class(cls):
        """ initialize a SparkSession """
        app_name: str = 'Total Customer Spend ETL Process'
        cls.spark = SparkSession.builder.appName(app_name).getOrCreate()

    def test_extract_success(self):
        file = 'customer-orders.csv'
        path = f'file://{Path().absolute()}/{file}'
        # path = f'hdfs://localhost:9000/user/sutter/data/{file}'  # read from Hadoop HDFS

        extractor = ExtractorCsv({'path': path})

        result: DataFrame = extractor.extract(TestExtractor.spark)

        assert len(result.collect()) == 10000
