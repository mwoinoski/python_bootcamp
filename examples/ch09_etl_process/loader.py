"""
Loader class implementation.
"""

from typing import ClassVar, List
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession


class Loader:
    """ Loader implements the "load" process of ETL """
    output_cols: ClassVar[List[str]] = ['Customer ID', 'Total Orders']

    def __init__(self):
        pass

    def load(self, spark: SparkSession, df: DataFrame):
        file = 'customer-orders-totals.csv'
        # write DataFrame as a single CSV text file instead of a distributed HDFS file
        df.toDF(*Loader.output_cols) \
          .toPandas() \
          .to_csv(file, header=True, index=False)
        # write the DataFrame as CSV to Hadoop HDFS
        # path = f'file://{Path().absolute()}/customer-orders-totals'
        # result_df.toDF('Customer ID', 'Total Orders') \
        # .write.csv(path, mode='overwrite', header=True)
