"""
Transform class implementation.
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import sum

from case_study.etl.transformer import Transformer


class TransformerCleanQipData(Transformer):
    """ Transform implements the "transform" process of ETL """

    def transform(self, spark: SparkSession, df: DataFrame) -> DataFrame:
        """ Apply transformations to a DataFrame """
        self.logger.info('Transform: clean QIP data')

        try:
            # Normalize column names
            for col in df.columns:
                new_name: str = self.normalize_column_name(col, 64)
                df = df.withColumnRenamed(col, new_name)

            # Remove Total Performance Scores of 'No Score'
            score: str = 'total_performance_score'
            df = df.where(df[score] != 'No Score') \
                   .withColumn(score, df[score].cast('integer'))

            return df

        finally:
            spark.stop()
