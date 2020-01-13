"""
Transform class implementation.
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import sum


class Transformer:
    """ Transform implements the "transform" process of ETL """

    def transform(self, spark: SparkSession, df: DataFrame) -> DataFrame:
        """ Apply transformations to a DataFrame """
        result_limit = 5
        result_df = df.toDF('cust_id', 'order_id', 'amount') \
            .select('cust_id', 'amount') \
            .groupBy('cust_id') \
            .agg(sum('amount').alias('total')) \
            .orderBy('total', ascending=False) \
            .limit(result_limit)
        return result_df
