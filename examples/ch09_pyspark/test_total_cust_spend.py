"""
Unit tests for ETL process Total Customer Spend
"""

from typing import List, Tuple, ClassVar
from pyspark.sql import SparkSession, DataFrame, Row
from pyspark.sql.functions import sum  # pylint: disable=no-name-in-module
from textwrap import dedent

from pytest import approx


def transform(df: DataFrame) -> DataFrame:
    result_limit = 5
    result_df = df.toDF('cust_id', 'order_id', 'amount') \
                  .select('cust_id', 'amount') \
                  .groupBy('cust_id') \
                  .agg(sum('amount').alias('total')) \
                  .orderBy('total', ascending=False) \
                  .limit(result_limit)
    return result_df


class TestEtlTotalCustSpend:
    spark: ClassVar[SparkSession]
    input_schema: str = \
        '`Customer ID` int, `Order ID` int, `Order Total` double'

    @classmethod
    def setup_class(cls):
        """ initialize a SparkSession """
        app_name: str = 'Total Customer Spend (unit test)'
        cls.spark = SparkSession.builder.appName(app_name).getOrCreate()

    def create_data_frame(self, csv_string: str) -> DataFrame:
        """ Read a CSV string into a DataFrame """
        # '    44, 8602, 37.19\n    35, 5368, 65.89\n     ...'

        csv_lines: List[str] = dedent(csv_string).split('\n')
        # ['44, 8602, 37.19', '35, 5368, 65.89', ...]

        records_of_strings: List[List[str]] = \
            [line.split(',') for line in csv_lines]
        # [['44', '8602', '37.19'], ['35', '5368', '65.89'], ...]

        records_of_numbers: List[Tuple[int, int, float]] = \
            [(int(rec[0]), int(rec[1]), float(rec[2]))
             for rec in records_of_strings]
        # [(44, 8602, 37.19), (35, 5368, 65.89), ...]

        return self.spark.createDataFrame(records_of_numbers,
                                          schema=self.input_schema)

    @staticmethod
    def assert_dataframe_contents(df: DataFrame,
                                  expected_values: List[Tuple[int, float]]):
        """ Compare each Row attribute to a value in a tuple """
        df_contents: List[Row] = df.collect()  # Row[int, float]
        df_values = [(row.cust_id, row.total) for row in df_contents]

        for df_value, expected_value in zip(df_values, expected_values):
            assert df_value == approx(expected_value)

    def test_transform_success(self) -> None:
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
        data_frame = self.create_data_frame(input_data)

        result: DataFrame = transform(data_frame)

        self.assert_dataframe_contents(result, [
            (53, 152.23),
            (44, 80.7),
            (35, 65.89),
            (2, 40.64),
            (91, 24.59),
        ])
