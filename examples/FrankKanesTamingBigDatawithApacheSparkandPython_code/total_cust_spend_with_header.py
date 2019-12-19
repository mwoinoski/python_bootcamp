"""
Calculate total spending by customer in customer-orders-with-header.csv
"""

from typing import List
from pyspark import SparkConf
from pyspark.sql import SparkSession, DataFrame, Row
from pyspark.sql.functions import sum as sum_col  # pylint: disable=no-name-in-module
import util


# initialize spark
ss: SparkSession = SparkSession.builder \
                               .appName('Total Customer Spend (CSV with header)') \
                               .getOrCreate()

file: str = 'customer-orders-with-header.csv'
df: DataFrame = ss.read.csv(util.file_url(file), 
                            inferSchema=True, header=True)

result: List[Row] = df.toDF('cust_id', 'order_id', 'amount') \
                      .select('cust_id', 'amount') \
                      .groupBy('cust_id') \
                      .agg(sum_col('amount').alias('total')) \
                      .orderBy('total') \
                      .collect()

for row in result:
    d = row.asDict()
    print(f"{d['cust_id']} {d['total']:.2f}")
    # print(f"{row[0]} {row[1]:.2f}")
