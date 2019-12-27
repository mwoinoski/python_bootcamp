"""
ETL demo.
Reads from SQLServer tables and writes to MySQL tables.
SQLServer database PyBootCamp, table Customer_Order
CREATE TABLE Customer_Order (customer_id INT, order_id INT, amount SMALLMONEY)
MySQL data etltarget. table

You must supply the paths to the jar files with the SQLServer and MySQL JDBC
drivers as the spark-submit options "--driver-class-path" and "--jars":
    spark-submit --driver-class-path $HOME/lib/mssql-jdbc-7.4.1.jre8.jar,$HOME/lib/mssql-jdbc-7.4.1.jre8.jar \
                 --jars $HOME/lib/mssql-jdbc-7.4.1.jre8.jar,$HOME/lib/mssql-jdbc-7.4.1.jre8.jar \
                  etl_demo.py
"""

from configparser import ConfigParser
from typing import Dict

from pyspark.sql import SparkSession, DataFrame, Window

# MW TODO: functional decomposition example/exercise: extract function, transform function, load function
#          Why? its's much easier to test small functions

input_table: str = 'esrd_qip'
output_table: str = 'esrd_qip_clean'

config: ConfigParser = ConfigParser()
config.read('config.ini')
mssql_conf: Dict[str, str] = config['mssql']
mysql_conf: Dict[str, str] = config['mysql']

# initialize spark
spark: SparkSession = SparkSession.builder \
                                  .appName('ESRD QIP ETL Demmo') \
                                  .getOrCreate()

print(f"Reading data from SQLServer {input_table.upper()} table at {mssql_conf['url']}")

# Read unfiltered data from SQLServer
input_df: DataFrame = spark.read.format('jdbc') \
        .option('dbtable', input_table) \
        .option('url', mssql_conf['url']) \
        .option('databaseName', mssql_conf['databaseName']) \
        .option('driver', mssql_conf['driver']) \
        .option('user', mssql_conf['user']) \
        .option('password', mssql_conf['password']) \
        .load()

print(f'Read {input_df.count()} records')

# In this case, some 'Total Performace Score' values are 'No Score', so the
# column is identified as a string type. We'll need to filter out the
# non-numeric values and then convert to integers.
score: str = 'Total Performance Score'
output_df: DataFrame = \
    input_df.where(input_df[score] != 'No Score') \
            .withColumn(score, input_df[score].cast('integer'))

print(f"Writing data to MySQL {output_table.upper()} table at {mysql_conf['url']}")

# Write the DataFrame to a new MySQL table
output_df.write.format('jdbc') \
         .option('dbtable', output_table) \
         .option('url', mysql_conf['url']) \
         .option('driver', mysql_conf['driver']) \
         .option('user', mysql_conf['user']) \
         .option('password', mysql_conf['password']) \
         .mode('overwrite') \
         .save()
# default mode is 'create' and raise error if table exists
# df.mode('append')  # add data to existing table
# df.mode('overwrite')  # overwrite existing data

print('Done')
