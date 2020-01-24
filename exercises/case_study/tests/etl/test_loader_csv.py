"""
Unit tests for Loader
"""
import os
from textwrap import dedent
from typing import ClassVar, List, Tuple
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession

from loader import LoaderCsv


class TestLoader:
    spark: ClassVar[SparkSession]
    output_file: ClassVar[str] = f'/tmp/test-etl-process-loader.csv'

    @classmethod
    def setup_class(cls):
        """ initialize a SparkSession """
        app_name: str = 'Total Customer Spend ETL Process'
        cls.spark = SparkSession.builder.appName(app_name).getOrCreate()

    def teardown_method(self, method):
        try:
            os.remove(TestLoader.output_file)
        except Exception:
            pass

    def test_load_success(self):
        input_data = """\
            44,37.19
            35,65.89
            2,40.64
            44,14.98
            29,13.08
            91,24.59
            53,68.68
            44,28.53
            53,83.55
            14,4.32"""
        data_frame: DataFrame = self.create_data_frame_from_csv_string(input_data)

        loader: LoaderCsv = LoaderCsv({'path': TestLoader.output_file})

        loader.write_to_db(TestLoader.spark, data_frame)

        path = f'file://{TestLoader.output_file}'
        df: DataFrame = TestLoader.spark.read.csv(path, header=True)
        assert len(df.collect()) == 10

    def create_data_frame_from_csv_string(self, csv_string: str) -> DataFrame:
        """ Read a CSV string into a DataFrame """
        csv_lines: List[str] = dedent(csv_string).split('\n')
        records_of_strings: List[List[str]] = \
            [line.split(',') for line in csv_lines]
        records_of_numbers: List[Tuple[int, float]] = \
            [(int(rec[0]), float(rec[1]))
             for rec in records_of_strings]

        return self.spark.createDataFrame(records_of_numbers,
            schema='`Customer ID` int, `Total Orders` float')
