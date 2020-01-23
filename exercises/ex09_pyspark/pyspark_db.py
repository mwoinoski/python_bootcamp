"""
PySpark application that reads and writes to databases.
Reads from a SQLServer table and writes to a MySQL table.

If you have write permission on $SPARK_HOME/jars, copy the SQLServer and MySQL
JDBC driver jar files to that directory.

If not, you must supply the paths to the jar files with the SQLServer and MySQL
JDBC drivers as the spark-submit options "--driver-class-path" and "--jars":
    spark-submit --driver-class-path $HOME/lib/mssql-jdbc-7.4.1.jre8.jar,$HOME/lib/mysql-connector-java-8.0.18.jar \
                 --jars $HOME/lib/mssql-jdbc-7.4.1.jre8.jar,$HOME/lib/mysql-connector-java-8.0.18.jar \
                 case_study/pyspark_db.py
"""

import re
import logging.config
from pyspark.sql import SparkSession, DataFrame

input_table_name: str = 'ESRD_QIP'
output_table_name: str = 'ESRD_QIP_CLEAN'
facility_csv_table: str =
logger: logging.Logger


def main():
    logger.info('process starting...')

    spark: SparkSession = initialize_spark_session()

    esrd_qip_df: DataFrame = read_from_db(input_table_name, spark)
    facility_df: DataFrame = read_from_csv(facility_csv_file, spark)
    output_df: DataFrame = clean_data(esrd_qip_df)
    write_to_db(output_df, output_table_name)

    logger.info('process complete')


def initialize_spark_session():
    spark: SparkSession = SparkSession.builder \
        .appName('PySpark_DB_Operations') \
        .getOrCreate()
    return spark


def read_from_db(table_name: str, spark: SparkSession) -> DataFrame:
    logger.info(f"Reading from SQLServer {table_name} table")
    # Read unfiltered data from SQLServer
    input_df: DataFrame = spark.read \
        .format('jdbc') \
        .option('dbtable', table_name) \
        .option('url', 'jdbc:sqlserver://localhost') \
        .option('databaseName', 'PyBootCamp') \
        .option('driver', 'com.microsoft.sqlserver.jdbc.SQLServerDriver') \
        .option('user', 'SA') \
        .option('password', '3#Sutter') \
        .load()
    logger.debug(f'Read {input_df.count()} records')
    return input_df


def clean_data(input_df: DataFrame) -> DataFrame:
    for col in input_df.columns:
        new_name: str = normalize_column_name(col, 64)
        input_df = input_df.withColumnRenamed(col, new_name)

    # Some 'Total Performace Score' values are 'No Score', so the
    # column's data type is string. We need to filter out the non-numeric
    # values and then convert the remaining values to integers.
    score: str = 'Total_Performance_Score'
    output_df: DataFrame = input_df.where(input_df[score] != 'No Score') \
        .withColumn(score, input_df[score].cast('integer'))
    return output_df


def normalize_column_name(name: str, max_len: int) -> str:
    name = name.lower()
    name = re.sub(r'\W', '_', name)
    name = name.strip('_')
    name = name[:max_len]
    return name


def write_to_db(output_df: DataFrame, table_name: str) -> None:
    logger.debug(f"Writing to MySQL {table_name} table")
    # Write the DataFrame to a new MySQL table
    output_df.write.format('jdbc') \
        .option('dbtable', table_name) \
        .option('url', 'jdbc:mysql://localhost/etltarget') \
        .option('driver', 'com.mysql.cj.jdbc.Driver') \
        .option('user', 'etltarget') \
        .option('password', '3#Sutter') \
        .mode('overwrite') \
        .save()
    # default mode is 'create', which raises error if table exists
    # df.mode('append')  # add data to existing table
    # df.mode('overwrite')  # overwrite existing data


if __name__ == '__main__':
    logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
    logger = logging.getLogger('pyspark_db')

    main()
