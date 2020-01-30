"""
Unit tests for Loader
"""

import os
import shutil
from textwrap import dedent
from typing import ClassVar, List, Any
from unittest.mock import patch

from pyspark.sql import DataFrame, SparkSession, Row

from case_study.etl.load.loader_csv import LoaderCsv


# patch the EtlLogger class (i.e., replace it with a mock). Remember
# to refer to the module that imported EtlLogger, not the module
# that defines EtlLogger
@patch('case_study.etl.load.loader_csv.EtlLogger')
class TestLoaderCsv:
    spark: ClassVar[SparkSession]
    output_file: ClassVar[str] = f'/tmp/test-etl-process-loader.csv'

    @classmethod
    def setup_class(cls):
        """ initialize a SparkSession """
        app_name: str = 'ETL Process Test'
        cls.spark = SparkSession.builder.appName(app_name).getOrCreate()

    def teardown_method(self, method):
        try:
            shutil.rmtree(TestLoaderCsv.output_file)
        except Exception:
            pass

    def test_load_success_small_dataset(self, mock_class):
        """
        This test case verifies the exact contents of an entire dataset.
        This technique is useful for checking a small, representative subset of
        the data to be processed.
        """

        # ARRANGE
        input_data = """
            CHILDRENS HOSPITAL DIALYSIS,012306,013300,1600 7TH AVENUE SOUTH,-,BIRMINGHAM,AL,35233,99
            GADSDEN DIALYSIS,012501,-,409 SOUTH FIRST STREET,-,GADSDEN,AL,35901,100
            TUSCALOOSA UNIVERSITY DIALYSIS,012502,-,220 15TH STREET,-,TUSCALOOSA,AL,35401,0
            DOTHAN DIALYSIS,012506,-,216 GRACELAND DR.,-,DOTHAN,AL,36305,88
        """
        input_df: DataFrame = self.create_data_frame_from_csv_string(input_data)

        # ACT
        loader: LoaderCsv = LoaderCsv({'path': TestLoaderCsv.output_file})
        loader.load(TestLoaderCsv.spark, input_df)

        # ASSERT
        path = f'file://{TestLoaderCsv.output_file}'
        df_from_loaded_csv: DataFrame = \
            TestLoaderCsv.spark.read.csv(path, header=True)

        assert df_from_loaded_csv.columns == [
            'facility_name', 'cms_certification_number_ccn', 'alternate_ccn_1', 'address_1',
            'address_2', 'city', 'state', 'zip_code', 'total_performance_score'
        ]
        self.assert_dataframe_contents(df_from_loaded_csv, [
            ['CHILDRENS HOSPITAL DIALYSIS', '012306', '013300', '1600 7TH AVENUE SOUTH', '-', 'BIRMINGHAM', 'AL', '35233', '99'],
            ['GADSDEN DIALYSIS', '012501', '-', '409 SOUTH FIRST STREET', '-', 'GADSDEN', 'AL', '35901', '100'],
            ['TUSCALOOSA UNIVERSITY DIALYSIS', '012502', '-', '220 15TH STREET', '-', 'TUSCALOOSA', 'AL', '35401', '0'],
            ['DOTHAN DIALYSIS', '012506', '-', '216 GRACELAND DR.', '-', 'DOTHAN', 'AL', '36305', '88'],
        ])

    def test_load_success_large_dataset(self, mock_class):
        """
        This test case verifies a few selected rows of a dataset.
        In this case, the dataset is very small, but the verification technique
        will work on much larger, production-scale load operations.
        """

        # ARRANGE
        input_data = """
            CHILDRENS HOSPITAL DIALYSIS,012306,013300,1600 7TH AVENUE SOUTH,-,BIRMINGHAM,AL,35233,99
            GADSDEN DIALYSIS,012501,-,409 SOUTH FIRST STREET,-,GADSDEN,AL,35901,100
            TUSCALOOSA UNIVERSITY DIALYSIS,012502,-,220 15TH STREET,-,TUSCALOOSA,AL,35401,0
            DOTHAN DIALYSIS,012506,-,216 GRACELAND DR.,-,DOTHAN,AL,36305,88
        """
        input_df: DataFrame = self.create_data_frame_from_csv_string(input_data)

        # ACT
        loader: LoaderCsv = LoaderCsv({'path': TestLoaderCsv.output_file})
        loader.load(TestLoaderCsv.spark, input_df)

        # ASSERT
        path = f'file://{TestLoaderCsv.output_file}'
        df: DataFrame = TestLoaderCsv.spark.read.csv(path, header=True)
        # TODO: you can replace the above statement with code to read from
        #       a database table; see case_study/etl/extract/extractor_db.py

        assert df.columns == [
            'facility_name', 'cms_certification_number_ccn', 'alternate_ccn_1', 'address_1',
            'address_2', 'city', 'state', 'zip_code', 'total_performance_score'
        ]
        assert df.count() == 4

        df.createOrReplaceTempView('loaded_data')  # used in SQL queries below

        # verify one value of one row
        result: Row = self.spark.sql("""
                select total_performance_score score 
                  from loaded_data
                 where cms_certification_number_ccn == '012306'
             """).collect()[0]
        assert result.score == '99'

        # assert df.select(df.total_performance_score) \
        #          .where(df.cms_certification_number_ccn == '012306')\
        #          .collect()[0] == '99'

        # verify that a record is not present (i.e., it should have been
        # filtered out by the tranform operation)
        assert not self.spark.sql("""
                select * 
                  from loaded_data
                 where cms_certification_number_ccn == '012307'
             """).collect()

    def create_data_frame_from_csv_string(self, csv_string: str) -> DataFrame:
        """ Read a CSV string into a DataFrame """

        schema_for_dataframe_to_be_loaded: ClassVar[str] = """
            facility_name string,
            cms_certification_number_ccn string,
            alternate_ccn_1 string,
            address_1 string,
            address_2 string,
            city string,
            state string,
            zip_code string,
            total_performance_score integer
        """

        csv_lines: List[str] = dedent(csv_string).split('\n')
        # Use a list comprehension to split all lines at commas, and
        # discard the blank first and last lines
        records: List[List[str]] = \
            [line.split(',') for line in csv_lines[1:-1]]
        for row in records:
            row[-1] = int(row[-1])  # convert last item to integer
        return self.spark.createDataFrame(records,
                    schema=schema_for_dataframe_to_be_loaded)

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
