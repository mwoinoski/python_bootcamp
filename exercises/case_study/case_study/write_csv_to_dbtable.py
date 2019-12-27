"""
Populates a DB table with the contents of a CSV file.

You must supply the paths to the jar files with the SQLServer and MySQL JDBC
drivers as the spark-submit options "--driver-class-path" and "--jars":
    spark-submit --driver-class-path $HOME/lib/mssql-jdbc-7.4.1.jre8.jar,$HOME/lib/mssql-jdbc-7.4.1.jre8.jar \
                 --jars $HOME/lib/mssql-jdbc-7.4.1.jre8.jar,$HOME/lib/mssql-jdbc-7.4.1.jre8.jar \
                  write_csv_to_dbtable.py
"""

from configparser import ConfigParser
from typing import Dict

from pyspark.sql import SparkSession, DataFrame, Window
import pyspark.sql.functions as f


dbms: str = 'mssql'
target_table: str = 'esrd_qip'
payment_year: str = '2018'
file: str = f'ESRD_QIP-Complete_QIP_Data-Payment_Year_2018.csv'
data_uri: str = 'hdfs://localhost:9000/user/sutter/data'

config: ConfigParser = ConfigParser()
config.read('config.ini')
conf: Dict[str, str] = config['mssql']  # 'mysql'

# initialize spark
spark: SparkSession = SparkSession.builder \
                                  .appName('Write CSV file to DB Table') \
                                  .getOrCreate()

path: str = f'{data_uri}/{file}'

df: DataFrame = spark.read \
                     .csv(path, inferSchema=True, header=True) \
                     .withColumn('payment_year', f.lit(payment_year))  # add column

print(f'Reading {df.count()} records from {path}')
print(f"Writing to {dbms.upper()} table {conf['dbtable'].upper()} at {conf['url']}")

df.write.format('jdbc') \
        .option('dbtable', target_table) \
        .option('url', conf['url']) \
        .option('databaseName', conf['databaseName']) \
        .option('driver', conf['driver']) \
        .option('user', conf['user']) \
        .option('password', conf['password']) \
        .mode('overwrite') \
        .save()

print('Done')
