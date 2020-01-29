"""
Transform class implementation.
"""

from pyspark.sql import DataFrame, SparkSession

from case_study.etl.transform.transformer import Transformer


class TransformerCleanQipData(Transformer):
    """ Transform implements the "transform" process of ETL """

    # in this case, we don't really need to define __init__, because it just
    # calls the superclass constructor, and python automatically calls the
    # superclass constructor if a subclass doesn't define __init__
    def __init__(self):
        """ Initialize the Transformer """
        super().__init__()

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

        except Exception as ex:
            self.logger.error(f'error while transforming: {ex}')
            raise
