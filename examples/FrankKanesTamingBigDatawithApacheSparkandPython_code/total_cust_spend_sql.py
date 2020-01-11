"""
Calculate total spending by customer in customer-orders.csv
"""

from typing import List
from pyspark.sql import SparkSession, DataFrame, Row
from pathlib import Path


# initialize Spark
app_name: str = 'Total Customer Spend (CSV)'
spark: SparkSession = SparkSession.builder \
                                  .appName(app_name) \
                                  .getOrCreate()

# Customer ID,Order ID,Order Total
# 44,8602,37.19
file: str = 'customer-orders.csv'
file_url: str = f'file://{str(Path().absolute())}/{file}'
print(f'\nReading customer spend data from {file_url}\n')

df: DataFrame = spark.read.csv(file_url, inferSchema=True, header=True) \
                          .cache()
# cache() persists the DataFrame to default storage level.
# Equivalent to persist(StorageLevel.MEMORY_AND_DISK)
# may help performance

df.createOrReplaceTempView('orders')

result_limit = 5
query = f"""
    SELECT `Customer ID` as cust_id, sum(`Order Total`) as total
      FROM orders
     GROUP BY cust_id
     ORDER BY total desc
     LIMIT {result_limit}
"""

query_df: DataFrame = spark.sql(query)

result: List[Row] = query_df.collect()

print(f'*** Top {result_limit} customers ***')
print(f'{"Customer ID":>11s}{"Total":>10s}')
for row in result:
    print(f'{row.cust_id:>11d} {row.total:>9.2f}')

spark.stop()
