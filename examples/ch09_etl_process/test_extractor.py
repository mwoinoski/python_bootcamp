"""
Unit tests for Extractor
"""
from typing import ClassVar
from unittest.mock import Mock

from pyspark.sql import DataFrame, SparkSession

from extractor import Extractor


class TestExtractor:
    spark: ClassVar[SparkSession]

    @classmethod
    def setup_class(cls):
        """ initialize a SparkSession """
        app_name: str = 'Total Customer Spend ETL Process'
        cls.spark = SparkSession.builder.appName(app_name).getOrCreate()

    def test_extract_success(self):
        extractor = Extractor()

        result: DataFrame = extractor.extract(TestExtractor.spark)

        assert len(result.collect()) == 10000
