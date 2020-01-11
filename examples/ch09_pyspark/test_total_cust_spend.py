"""
Calculate total spending by customer in customer-orders.csv
"""

from typing import List
from pyspark.sql import SparkSession, DataFrame, Row
from pyspark.sql.functions import sum  # pylint: disable=no-name-in-module
from pathlib import Path
from textwrap import dedent


# initialize Spark
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

app_name: str = 'Total Customer Spend (CSV)'
spark: SparkSession = SparkSession.builder \
                                  .appName(app_name) \
                                  .getOrCreate()

data_schema = StructType([
    StructField("Customer ID", IntegerType()),
    StructField("Order ID", IntegerType()),
    StructField("Order Total", DoubleType())
])

input_data = """\
    44,8602,37.19
    35,5368,65.89
    2,3391,40.64
    47,6694,14.98
    29,680,13.08
    91,8900,24.59
    70,3959,68.68
    85,1733,28.53
    53,9900,83.55
    14,1505,4.32"""

records = [line.split(',') for line in dedent(input_data).split('\n')]

df: DataFrame = spark.createDataFrame(records, schema=data_schema)

# file: str = 'customer-orders.csv'
# file_url: str = f'file://{Path().absolute()}/{file}'
#
# file_schema = '`Customer ID` integer, `Order ID` integer, `Order Total` double'
# df: DataFrame = spark.read.csv(file_url, header=True, schema=file_schema)

result_limit = 5
result_df = df.toDF('cust_id', 'order_id', 'amount') \
              .select('cust_id', 'amount') \
              .groupBy('cust_id') \
              .agg(sum('amount').alias('total')) \
              .orderBy('total', ascending=False) \
              .limit(result_limit)
result: List[Row] = result_df.collect()

print(f'*** Top {result_limit} customers ***')
print(f'{"Customer ID":>11s}{"Total":>10s}')

for row in result:
    cust_id = row.cust_id
    cust_total = row.total
    print(f"{cust_id} {cust_total:.2f}")

    # d = row.asDict()
    # print(f"{d['cust_id']:>11d} {d['total']:>9.2f}")

    # print(f"{row[0]} {row[1]:.2f}")
