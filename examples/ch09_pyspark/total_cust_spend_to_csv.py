"""
Calculate total spending by customer in customer-orders.csv
"""

from typing import List
from pyspark.sql import SparkSession, DataFrame, Row
from pyspark.sql.functions import sum  # pylint: disable=no-name-in-module
from pathlib import Path


# initialize Spark
app_name: str = 'Total Customer Spend (CSV)'
spark: SparkSession = SparkSession.builder \
                                  .appName(app_name) \
                                  .getOrCreate()

input_file: str = 'customer-orders.csv'
output_file: str = 'customer-orders-totals.csv'

url_template = f'file://{Path().absolute()}/'
input_path: str = url_template + input_file
output_path: str = url_template + output_file

print(f'\nReading customer spend data from {input_path}\n')

input_schema = '`Customer ID` integer, `Order ID` integer, `Order Total` double'
df: DataFrame = spark.read.csv(input_path, header=True, schema=input_schema)

result_df = df.toDF('cust_id', 'order_id', 'amount') \
              .select('cust_id', 'amount') \
              .groupBy('cust_id') \
              .agg(sum('amount').alias('total')) \
              .orderBy('total', ascending=False)

# write DataFrame as a single CSV text file instead of a distributed HDFS file
result_df.toDF('Customer ID', 'Total Orders') \
         .toPandas().to_csv(output_file, header=True, index=False)

# write the DataFrame as CSV to Hadoop HDFS
# result_df.toDF('Customer ID', 'Total Orders') \
# .write.csv(re.sub(r'\.[^.]+$', '', output_path), mode='overwrite', header=True)

# write to temp file: df.write.csv(os.path.join(tempfile.mkdtemp(), 'data'))
