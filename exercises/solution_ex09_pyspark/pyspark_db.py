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
import pyspark.sql.functions as f

input_table_name: str = 'esrd_qip'
provider_csv_file: str = 'provider_credentials_data.csv'
output_table_name: str = 'active_providers'
logger: logging.Logger


def main():
    logger.info('process starting...')

    spark: SparkSession = initialize_spark_session()

    facility_df: DataFrame = read_from_db(input_table_name, spark)
    provider_df: DataFrame = read_from_csv(provider_csv_file, spark)
    output_df: DataFrame = join_dataframes(facility_df, provider_df, spark)
    output_df.show()
    write_to_db(output_df, output_table_name)
    spark.stop()
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


def read_from_csv(path: str, spark: SparkSession) -> DataFrame:
    logger.info(f"Reading from CSV file {path}")
    df = spark.read.csv(path, inferSchema=True, header=True)
    logger.debug(f'Read {df.count()} records')
    return df


def join_dataframes(facility_df: DataFrame, provider_df: DataFrame,
                    spark: SparkSession) -> DataFrame:

    for col in facility_df.columns:
        new_name: str = normalize_column_name(col, 64)
        facility_df = facility_df.withColumnRenamed(col, new_name)

    # Some 'Total Performace Score' values are 'No Score', so the
    # column's data type is string. We need to filter out the non-numeric
    # values and then convert the remaining values to integers.
    score: str = 'total_performance_score'
    facility_df = facility_df.where(facility_df[score] != 'No Score') \
        .withColumn(score, facility_df[score].cast('integer'))

    for col in provider_df.columns:
        new_name: str = normalize_column_name(col, 64)
        provider_df = provider_df.withColumnRenamed(col, new_name)

    # TODO: join facility_df and provider_df on Facility Certification Number,
    #       then select active providers from facilities whose
    #       Total Performance Score is greater than 90
    # HINT: facility column names:
    #          facility_name
    #          cms_certification_number_cnn (maps to provider's facilitycertnum)
    #          total_performance_score
    #      provider column names:
    #          credentialnumber
    #          firstname
    #          lastname
    #          status
    #          facilitycertnum (maps to facility's cms_certification_number_cnn)

    facility_df.createOrReplaceTempView('facility')
    provider_df.createOrReplaceTempView('provider')
    query = """
        select fac.facility_name, prov.credentialnumber, prov.firstname,
               prov.lastname, prov.status
          from facility fac
          join provider prov
            on fac.cms_certification_number_ccn = prov.facilitycertnum
         where fac.total_performance_score > 90
               and lower(prov.status) = 'active'
    """
    output_df = spark.sql(query)

    # output_df = provider_df.join(facility_df,
    #                              facility_df.cms_certification_number_ccn == \
    #                              provider_df.facilitycertnum) \
    #     .select(facility_df.facility_name, provider_df.firstname,
    #             provider_df.lastname, provider_df.status) \
    #     .where((facility_df.total_performance_score > 90) &
    #            (f.lower(provider_df.status) == 'active'))

    logger.debug(f'join produced {output_df.count()} records')
    return output_df

    # SQLServer querys for ESRD_QIP table:
    # select [CMS Certification Number (CCN)] from esrd_qip where city = 'Sacramento'
    # select [Facility Name] from esrd_qip where [CMS Certification Number (CCN)] = 12500


def normalize_column_name(name: str, max_len: int) -> str:
    name = name.lower()
    name = re.sub(r'\W', '_', name)
    name = re.sub(r'__+', '_', name)
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
