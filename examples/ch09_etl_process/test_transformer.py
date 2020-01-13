"""
Unit tests for Transformer
"""

from typing import List, ClassVar, Tuple
from unittest.mock import Mock

from pyspark.sql import SparkSession, DataFrame, Row
from textwrap import dedent

from pytest import approx, raises

from transformer import TransformerTopFiveCust
from etl_process import EtlProcessError


class TestTransformer:
    spark: ClassVar[SparkSession]
    input_schema: str = \
        '`Customer ID` int, `Order ID` int, `Order Total` double'

    @classmethod
    def setup_class(cls):
        """ initialize a SparkSession """
        app_name: str = 'Total Customer Spend ETL Process'
        cls.spark = SparkSession.builder.appName(app_name).getOrCreate()

    def test_transform_success(self):
        input_data = """\
            44,8602,37.19
            35,5368,65.89
            2,3391,40.64
            44,6694,14.98
            29,680,13.08
            91,8900,24.59
            53,3959,68.68
            44,1733,28.53
            53,9900,83.55
            14,1505,4.32"""
        initial_df: DataFrame = self.create_data_frame_from_csv_string(input_data)

        transformer = TransformerTopFiveCust()
        transformed_dataframe: DataFrame = transformer.transform(spark=Mock(),
                                                                 df=initial_df)

        self.assert_dataframe_contents(transformed_dataframe, [
            (53, 152.23),
            (44, 80.7),
            (35, 65.89),
            (2, 40.64),
            (91, 24.59),
        ])

    def create_data_frame_from_csv_string(self, csv_string: str) -> DataFrame:
        """ Read a CSV string into a DataFrame """
        csv_lines: List[str] = dedent(csv_string).split('\n')
        records_of_strings: List[List[str]] = \
            [line.split(',') for line in csv_lines]
        records_of_numbers: List[Tuple[int, int, float]] = \
            [(int(rec[0]), int(rec[1]), float(rec[2]))
             for rec in records_of_strings]
        return self.spark.createDataFrame(records_of_numbers,
                                          schema=self.input_schema)

    @staticmethod
    def assert_dataframe_contents(df: DataFrame,
                                  expected_values: List[Tuple[int, float]]):
        """ Compare each Row attribute to a value in a tuple """
        df_contents: List[Row] = df.collect()  # Row[int, float]
        df_values = [(row[0], row[1]) for row in df_contents]

        for df_value, expected_value in zip(df_values, expected_values):
            assert df_value == approx(expected_value)
