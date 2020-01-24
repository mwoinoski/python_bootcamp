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

# TODO: note the imports of the Spark modules
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as f

# TODO: note the global variables that define the table and file names
input_table_name: str = 'esrd_qip'
input_csv_file: str = 'provider_credentials_data.csv'
output_table_name: str = 'active_providers'

logger: logging.Logger


# TODO: note the defintion of the main function (it's called at the end of the file)
def main():
    logger.info('process starting...')

    spark: SparkSession = initialize_spark_session()

    try:
        # TODO: note the following sequence of function calls:
        #       1. Read from SQLServer
        #       2. Read from CSV file
        #       3. Join the two DataFrames
        #       4. Write the result to MySQL
        facility_df: DataFrame = read_from_db(input_table_name, spark)

        provider_df: DataFrame = read_from_csv(input_csv_file, spark)

        output_df: DataFrame = join_dataframes(facility_df, provider_df, spark)

        write_to_db(output_df, output_table_name)
    finally:
        spark.stop()

    logger.info('process completed successfully')


def initialize_spark_session():
    """ Get a SparkSession"""
    spark: SparkSession = SparkSession.builder \
        .appName('PySpark_DB_Operations') \
        .getOrCreate()
    return spark


def read_from_db(table_name: str, spark: SparkSession) -> DataFrame:
    """ Read unfiltered data from SQLServer """
    logger.info(f"Reading from SQLServer {table_name} table")
    # TODO: note how you extract a DataFrame from a SQLServer table
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


def read_from_csv(filename: str, spark: SparkSession) -> DataFrame:
    """ Read a CSV file from Hadoop file system """
    logger.info(f"Reading from CSV file {filename}")
    url = f'hdfs://localhost:9000/user/sutter/data/'
    # TODO: create the path by concatenating the URL and the filename
    path = ....
    # TODO: read the CSV file from the path
    # HINT: be sure that Spark know the file has a header
    # HINT: tell Spark to determine the datatypes of the columns
    # HINT: be sure to cache the DataFrame so you can create a temp view later
    df = ....
    logger.debug(f'Read {df.count()} records from CSV file')
    # TODO: return the DataFrame that you just read
    return ....


def join_dataframes(facility_df: DataFrame, provider_df: DataFrame,
                    spark: SparkSession) -> DataFrame:
    """ Transform and join two DataFrames """

    #  Normalize the column names
    # TODO: loop over all the column names in facility_df
    for col in ....
        # TODO: pass each column name to the normalize_column_name function
        new_name: str = normalize_column_name(....)
        facility_df = facility_df.withColumnRenamed(col, new_name)

    # Some 'Total Performace Score' values are 'No Score', so the
    # column's data type is string. You need to filter out the non-numeric
    # values and then convert the remaining values to integers.
    score: str = 'total_performance_score'
    facility_df = facility_df.where(facility_df[score] != 'No Score') \
        .withColumn(score, facility_df[score].cast('integer'))

    # TODO: loop over all the column names in provider_df
    # HINT: provider_df.columns is a list of all the column names
    for ....
        # TODO: pass each column name to the normalize_column_name function
        new_name = ....
        provider_df = provider_df.withColumnRenamed(col, new_name)

    # TODO: use facility_df to create or replace a temp view named 'facility'
    facility_df....
    # TODO: use provider_df to create or replace a temp view named 'provider'
    ....

    # TODO: Write a SQL query that selects a facility's name and performance score,
    #       and a provider's first name, last name, and status.
    #       Join facility and provider on CMS Certification Number,
    #       then select providers from facilities where the
    #       facility's Total Performance Score is greater than 90 and
    #       the provider's status is 'ACTIVE'
    # HINT: facility column names:
    #          facility_name
    #          cms_certification_number_cnn (maps to provider's facilitycertnum)
    #          total_performance_score
    #      provider column names:
    #          credentialnumber
    #          firstname
    #          lastname
    #          status
    #          facilitycertnum (foreign key on facility's cms_certification_number_cnn)

    query = """
        ....
    """
    # TODO: execute the query to create a DataFrame
    output_df = ....

    # BONUS TODO: comment out the SQL query you wrote, and re-write the
    #             join operation using the DataFrame Python API
    # HINT:       look in the PySpark documentation for examples of
    #             the DataFrame join() method

    logger.debug(f'join produced {output_df.count()} records')
    if logger.getEffectiveLevel() == logging.DEBUG:
        output_df.show()
    return output_df

    # SQLServer querys for ESRD_QIP table:
    # select [CMS Certification Number (CCN)] from esrd_qip where city = 'Sacramento'
    # select [Facility Name] from esrd_qip where [CMS Certification Number (CCN)] = 12500


def normalize_column_name(name: str, max_len: int = 64) -> str:
    """ Normalize a column name """
    name = name.lower()
    name = re.sub(r'\W', '_', name)
    name = re.sub(r'__+', '_', name)
    name = name.strip('_')
    name = name[:max_len]
    return name


def write_to_db(output_df: DataFrame, table_name: str) -> None:
    """ Create/overwrite a MySQL table """
    logger.info(f"Writing to MySQL {table_name} table")
    # TODO: note how you write a DataFrame to a database table
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
    logger.debug(f'Wrote {output_df.count()} records')


if __name__ == '__main__':
    logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
    logger = logging.getLogger('pyspark_db')

    # TODO: note the call to the main function
    main()
