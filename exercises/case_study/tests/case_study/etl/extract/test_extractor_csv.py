"""
Unit tests for Extractor
"""

from typing import ClassVar, Any, Dict
from pathlib import Path
from unittest.mock import patch

from pyspark.sql import DataFrame, SparkSession

from case_study.etl.extract.extractor_csv import ExtractorCsv


# patch the EtlLogger class (i.e., replace it with a mock). Remember
# to refer to the module that imported EtlLogger, not the module
# that defines EtlLogger
@patch('case_study.etl.extract.extractor_csv.EtlLogger')
class TestExtractor:
    spark: ClassVar[SparkSession]

    @classmethod
    def setup_class(cls):
        """ initialize a SparkSession """
        app_name: str = 'ETL Process Test'
        cls.spark = SparkSession.builder.appName(app_name).getOrCreate()

    # because of @patch on the class, all test methods need an addtional
    # argument, but we can safely ignore it
    def test_extract_success(self, mock_class):
        file = 'ESRD_QIP-Complete_QIP_Data-Payment_Year_2018.csv'
        path = f'file://{Path().absolute()}/tests/case_study/etl/extract/data/{file}'
        # path = f'hdfs://localhost:9000/user/sutter/data/{file}'  # read from Hadoop HDFS

        extractor = ExtractorCsv({'path': path})

        result: DataFrame = extractor.extract(TestExtractor.spark)

        assert len(result.collect()) == 1000
