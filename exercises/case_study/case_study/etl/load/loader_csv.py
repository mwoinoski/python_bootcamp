"""
Loader class implementation.
"""

from typing import ClassVar, List, Dict, Any
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession

from case_study.etl.etl_logger import EtlLogger


class LoaderCsv:
    """ Loader implements the "load" process of ETL """
    output_cols: ClassVar[List[str]] = ['Customer ID', 'Total Orders']
    logger: EtlLogger
    path: str

    def __init__(self, config: Dict[str, Any]):
        """ Initialize the Loader """
        self.path = config['path']
        self.logger = EtlLogger()

    def load(self, spark: SparkSession, df: DataFrame):
        """ Load the DataFrame to a CSV file """
        self.logger.debug(f'Load: {self.path}')

        try:
            # Write the CSV file to a distributed HDFS file. This produces
            # a Hadoop directory on the local disk, not just a single text file
            path = f'file://{Path().absolute()}/data/customer-orders-totals'
            df.write.csv(path, mode='overwrite', header=True)

            # Convert Spark DataFrame to Pandas DataFrame, because Pandas can write
            # to a single, plain CSV file instead of writing a distributed HDFS file
            # (for demo purposes only; usually HDFS is the right way to go)
            # df.toDF(*LoaderCsv.output_cols) \
            #   .toPandas() \
            #   .to_csv(self.path, header=True, index=False)

            # write the DataFrame as CSV to Hadoop HDFS:
            # path = f'hdfs://localhost:9000/user/sutter/data/customer-orders-totals'
            # df.toDF('Customer ID', 'Total Orders') \
            #   .write.csv(path, mode='overwrite', header=True)

            self.logger.debug(f'wrote {df.count()} rows to {self.path}')
        except Exception as ex:
            self.logger.error(f'error while loading {self.path}')
            raise
