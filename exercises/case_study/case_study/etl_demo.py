"""
ETL demo.
Reads from SQLServer tables and writes to MySQL tables.
SQLServer database PyBootCamp, table Customer_Order
CREATE TABLE Customer_Order (customer_id INT, order_id INT, amount SMALLMONEY)
MySQL data etltarget. table

You must supply the paths to the jar files with the SQLServer and MySQL JDBC
drivers as the spark-submit options "--driver-class-path" and "--jars":
    spark-submit --driver-class-path $HOME/lib/mssql-jdbc-7.4.1.jre8.jar,$HOME/lib/mysql-connector-java-8.0.18.jar \
                 --jars $HOME/lib/mssql-jdbc-7.4.1.jre8.jar,$HOME/lib/mysql-connector-java-8.0.18.jar \
                 case_study/etl_demo.py
"""
import re
from configparser import ConfigParser
from typing import Dict

from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as f

# MW TODO: functional decomposition example/exercise: extract function, transform function, load function
#          Why? its's much easier to test small functions

config: ConfigParser = ConfigParser()
config.read('config.ini')
extract_conf: Dict[str, str] = config['extract']
load_conf: Dict[str, str] = config['load']

# initialize spark
spark: SparkSession = SparkSession.builder \
                                  .appName('ESRD QIP ETL Demmo') \
                                  .getOrCreate()

# EXTRACT

input_table: str = 'esrd_qip'
print(f"Extracting from SQLServer {input_table.upper()} table "
      f"at {extract_conf['url']}")

# MW TODO convert to dict, pass as config options

# Read unfiltered data from SQLServer
input_df: DataFrame = spark.read.format(extract_conf['format']) \
        .option('dbtable', input_table) \
        .option('url', extract_conf['url']) \
        .option('databaseName', extract_conf['databaseName']) \
        .option('driver', extract_conf['driver']) \
        .option('user', extract_conf['user']) \
        .option('password', extract_conf['password']) \
        .load()

print(f'Read {input_df.count()} records')

# TRANSFORM


def normalize_column_name(name: str, max_len: int) -> str:
    name = name.lower()
    name = re.sub(r'\W', '_', name)
    name = name.strip('_')
    name = name[:max_len]
    return name


# MW TODO example/exercise
for col in input_df.columns:
    new_name: str = normalize_column_name(col, 64)
    # MW TODO: handle long names that are dupes after truncation
    input_df = input_df.withColumnRenamed(col, new_name)

# renamed_cols = [f.col(c).alias(re.sub(r'\W', '_', c[:64].strip()))
#                 for c in input_df.columns]
# input_df = input_df.select(renamed_cols)

# In this case, some 'Total Performace Score' values are 'No Score', so the
# column is identified as a string type. We'll need to filter out the
# non-numeric values and then convert to integers.
score: str = 'Total_Performance_Score'
output_df: DataFrame = \
    input_df.where(input_df[score] != 'No Score') \
            .withColumn(score, input_df[score].cast('integer'))

# LOAD

output_table: str = 'esrd_qip_clean'
print(f"Loading MySQL {output_table.upper()} table at {load_conf['url']}")

# Write the DataFrame to a new MySQL table
output_df.write.format(load_conf['format']) \
         .option('dbtable', output_table) \
         .option('url', load_conf['url']) \
         .option('driver', load_conf['driver']) \
         .option('user', load_conf['user']) \
         .option('password', load_conf['password']) \
         .mode('overwrite') \
         .save()
# default mode is 'create' and raise error if table exists
# df.mode('append')  # add data to existing table
# df.mode('overwrite')  # overwrite existing data

print('Done')
