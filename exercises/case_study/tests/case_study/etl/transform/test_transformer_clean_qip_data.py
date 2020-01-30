"""
Unit tests for Transformer
"""

from typing import List, ClassVar, Tuple, Any
from unittest.mock import Mock, patch

from pyspark.sql import SparkSession, DataFrame, Row
from textwrap import dedent

from pytest import raises

from case_study.etl.transform.transformer_clean_qip_data import (
    TransformerCleanQipData
)


# patch the EtlLogger class (i.e., replace it with a mock). Remember
# to refer to the module that imported EtlLogger, not the module
# that defines EtlLogger
@patch('case_study.etl.transform.transformer.EtlLogger')
class TestTransformerCleanQipData:
    spark: ClassVar[SparkSession]
    input_schema: ClassVar[str] = """
        `Facility Name` string,
        `CMS Certification Number (CCN)` string,
        `Alternate CCN 1` string,
        `Address 1` string,
        `Address 2` string,
        `City` string,
        `State` string,
        `Zip Code` string,
        `Total Performance Score` string
    """

    @classmethod
    def setup_class(cls):
        """ initialize a SparkSession """
        app_name: str = 'ETL Process Test'
        cls.spark = SparkSession.builder.appName(app_name).getOrCreate()

    # because of @patch on the class, all test methods need an addtional
    # argument, but we can safely ignore it
    def test_transform_success(self, mock_class):
        input_data = """
            CHILDRENS HOSPITAL DIALYSIS,012306,013300,1600 7TH AVENUE SOUTH,-,BIRMINGHAM,AL,35233,99
            FMC CAPITOL CITY,012500,-,255 S JACKSON STREET,-,MONTGOMERY,AL,36104,No Score
            GADSDEN DIALYSIS,012501,-,409 SOUTH FIRST STREET,-,GADSDEN,AL,35901,100
            TUSCALOOSA UNIVERSITY DIALYSIS,012502,-,220 15TH STREET,-,TUSCALOOSA,AL,35401,0
            PCD MONTGOMERY,012505,-,1001 FOREST AVENUE,-,MONTGOMERY,AL,36106,No Score
            DOTHAN DIALYSIS,012506,-,216 GRACELAND DR.,-,DOTHAN,AL,36305,88
        """

        initial_df: DataFrame = self.create_data_frame_from_csv_string(input_data)

        transformer = TransformerCleanQipData()
        transformed_dataframe: DataFrame = \
            transformer.transform(spark=Mock(spec=SparkSession),
                                  df=initial_df)

        assert transformed_dataframe.columns == [
            'facility_name', 'cms_certification_number_ccn', 'alternate_ccn_1', 'address_1',
            'address_2', 'city', 'state', 'zip_code', 'total_performance_score'
        ]
        self.assert_dataframe_contents(transformed_dataframe, [
            ['CHILDRENS HOSPITAL DIALYSIS', '012306', '013300', '1600 7TH AVENUE SOUTH', '-', 'BIRMINGHAM', 'AL', '35233', 99],
            ['GADSDEN DIALYSIS', '012501', '-', '409 SOUTH FIRST STREET', '-', 'GADSDEN', 'AL', '35901', 100],
            ['TUSCALOOSA UNIVERSITY DIALYSIS', '012502', '-', '220 15TH STREET', '-', 'TUSCALOOSA', 'AL', '35401', 0],
            ['DOTHAN DIALYSIS', '012506', '-', '216 GRACELAND DR.', '-', 'DOTHAN', 'AL', '36305', 88],
        ])

    def create_data_frame_from_csv_string(self, csv_string: str) -> DataFrame:
        """ Read a CSV string into a DataFrame """
        csv_lines: List[str] = dedent(csv_string).split('\n')
        # Use a list comprehension to split all lines at commas, and
        # discard the blank first and last lines
        records: List[List[str]] = \
            [line.split(',') for line in csv_lines[1:-1]]
        return self.spark.createDataFrame(records,
            schema=TestTransformerCleanQipData.input_schema)

    @staticmethod
    def assert_dataframe_contents(df: DataFrame,
                                  expected_values: List[List[Any]]):
        """ Compare each Row attribute to a value in a tuple """
        df_contents: List[Row] = df.collect()  # Row[str, str, ...]
        # convert the list of Rows to a list of lists
        df_col_count = len(df_contents[0].asDict().keys())
        df_values = [[row[i] for i in range(0, df_col_count)]
                     for row in df_contents]

        for df_value, expected_value in zip(df_values, expected_values):
            assert df_value == expected_value
