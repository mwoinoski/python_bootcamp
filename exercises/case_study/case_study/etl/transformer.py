"""
Transform class implementation.
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import sum
from etl_logger import EtlLogger


class TransformerTopFiveCust:
    """ Transform implements the "transform" process of ETL """
    logger: EtlLogger

    def __init__(self):
        self.logger = EtlLogger()

    def transform(self, spark: SparkSession, df: DataFrame) -> DataFrame:
        """ Apply transformations to a DataFrame """
        self.logger.info('Transform: top 5 customer totals')

        result_limit = 5
        result_df = df.toDF('cust_id', 'order_id', 'amount') \
                      .select('cust_id', 'amount') \
                      .groupBy('cust_id') \
                      .agg(sum('amount').alias('total')) \
                      .orderBy('total', ascending=False) \
                      .limit(result_limit)
        return result_df
