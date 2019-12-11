"""
Calculate total spending by customer. Customer order data is read from
SQLServer database PyBootCamp, table Customer_Order
CREATE TABLE Customer_Order (customer_id INT, order_id INT, amount SMALLMONEY)

You must supply the path to the jar file with the SQLServer JDBC driver
as the spark-submit options "--driver-class-path" and "--jars":
    spark-submit --driver-class-path mssql-jdbc-7.4.1.jre8.jar \
                 --jars mssql-jdbc-7.4.1.jre8.jar total_cust_spend_from_db.py
"""

from typing import List
from argparse import Namespace

from pyspark.sql import SparkSession, DataFrame, Row
from pyspark.sql.functions import desc
# from pyspark.sql.functions import sum as sum_col  # pylint: disable=no-name-in-module
from util import get_db_credentials

# Initialize spark.
# Note: In client mode, spark.driver.extraClassPath must not be set through
# the SparkConf directly in your application, because the driver JVM has already
# started at that point.
spark: SparkSession = SparkSession.builder \
        .appName('Total Customer Spend (SQLServer)') \
        .getOrCreate()

creds: Namespace = get_db_credentials()

df: DataFrame = spark.read.format("jdbc") \
        .option("url", "jdbc:sqlserver://localhost") \
        .option("dbtable", "customer_order") \
        .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
        .option("databaseName", "PyBootCamp") \
        .option("user", creds.user) \
        .option("password", creds.password) \
        .load()

# This also works:
# df: DataFrame = spark.read.jdbc(
#         url="jdbc:sqlserver://localhost",
#         table="customer_order",
#         properties={
#             "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
#             "databaseName": "PyBootCamp"
#             "user": creds.user,
#             "password": creds.password,
#         })

# Register the DataFrame as a SQL temporary view.
# Use the argument to createOrReplaceTempView() as the table name in the
# SELECT statement.
df.createOrReplaceTempView("customer_order")
query: str = """
      SELECT customer_id, SUM(amount) AS total
        FROM customer_order
    GROUP BY customer_id
    ORDER BY total
"""
resultDF: DataFrame = spark.sql(query)

# This also works:
# resultDF: DataFrame = df.select('customer_id', 'amount') \
#                         .groupBy('customer_id') \
#                         .agg(sum_col('amount').alias('total')) \
#                         .orderBy('total')

result: List[Row] = resultDF.collect()

row: Row
for row in result:
    d = row.asDict()
    print(f"{d['customer_id']} {d['total']:.2f}")
