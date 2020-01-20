"""
Transform class implementation.
"""

from pyspark.sql import DataFrame


class Transformer:
    """ Transform implements the "transform" process of ETL """

    def __init__(self):
        pass

    def transform(self, df: DataFrame) -> DataFrame:
        """ Apply transformations to a DataFrame """
        return df
