"""
Loader class implementation.
"""

from typing import ClassVar, List, Dict, Any
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession

from case_study.etl.etl_logger import EtlLogger


class LoaderDb:
    """ Loader implements the "load" process of ETL """
    output_cols: ClassVar[List[str]] = ['Customer ID', 'Total Orders']
    logger: EtlLogger
    path: str

    def __init__(self, config: Dict[str, Any]):
        """ Initialize the Loader """
        self.path = config['path']
        self.logger = EtlLogger()

    def load(self, spark: SparkSession, df: DataFrame):
        """ Load the DataFrame to a database table file """
        self.logger.debug(f'Load: {self.path}')

        try:
            raise NotImplementedError()
            # TODO: write DataFrame to database table
            # self.logger.debug(f'wrote {df.count()} rows to {self.path}')
        except Exception as ex:
            self.logger.error(f'error while loading {self.path}')
            raise
