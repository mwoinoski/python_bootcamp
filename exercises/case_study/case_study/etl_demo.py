"""
ETL demo.
Reads from SQLServer tables and writes to MySQL tables.

If you have write permission on $SPARK_HOME/jars, copy the SQLServer and MySQL
JDBC driver jar files to that directory.

If not, you must supply the paths to the jar files with the SQLServer and MySQL
JDBC drivers as the spark-submit options "--driver-class-path" and "--jars":
    spark-submit --driver-class-path $HOME/lib/mssql-jdbc-7.4.1.jre8.jar,$HOME/lib/mysql-connector-java-8.0.18.jar \
                 --jars $HOME/lib/mssql-jdbc-7.4.1.jre8.jar,$HOME/lib/mysql-connector-java-8.0.18.jar \
                 case_study/etl_demo.py
"""
import re
from argparse import ArgumentParser, Namespace
from configparser import ConfigParser
import logging
import logging.config

from typing import Dict

from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as f

# MW TODO: functional decomposition example/exercise: extract function, transform function, load function
#          Why? its's much easier to test small functions

# MW TODO: convert to class

# MW TODO: send email in case of errors
#          https://realpython.com/python-send-email/

default_config_file: str = 'config.ini'
logging_config_file: str = 'logging.ini'
logger_name: str = 'etl_demo'  # MW TODO: replace with EtlDemo.__module__
mode: str = 'prod'
logger: logging.Logger


def normalize_column_name(name: str, max_len: int) -> str:
    name = name.lower()
    name = re.sub(r'\W', '_', name)
    name = name.strip('_')
    name = name[:max_len]
    return name


def main():
    global default_config_file, mode, logger, \
        logging_config_file, logger_name

    logging.config.fileConfig(logging_config_file)
    logger = logging.getLogger(logger_name)

    logger.info('Starting ETL process')

    parser: ArgumentParser = ArgumentParser(description='Run ETL Process')
    help_msg: str = f'path to config file (defaults to {default_config_file})'
    parser.add_argument('-c', '--config-file', type=str, help=help_msg)
    parser.add_argument('-m', '--mode', type=str, help='dev, test, or prod')
    args: Namespace = parser.parse_args()
    # don't define a default value for the --mode argument: we need to know
    # if they set the mode explicitly
    if args.mode:
        mode = args.mode
    # MW TODO to test argument parsing: args = parser.parse_args(sys.argv),
    #         test values with vars(args).get('arg_name')

    # if --config-file is set, read that file.
    # otherwise, if --mode is set, read the file with the mode in the name.
    # otherwise, read the default file.
    config_file = default_config_file
    if args.config_file:
        config_file = args.config_file
    elif args.mode:
        name_ext = default_config_file.split('.')
        config_file = f'{name_ext[0]}-{args.mode}.{name_ext[1]}'

    config: ConfigParser = ConfigParser()
    if not config.read(config_file):
        raise Exception(f"couldn't read config file {config_file}")

    extract_conf: Dict[str, str] = config['extract']
    load_conf: Dict[str, str] = config['load']

    # initialize spark
    spark: SparkSession = SparkSession.builder \
                                      .appName('ESRD QIP ETL Demmo') \
                                      .getOrCreate()

    # EXTRACT

    input_table: str = 'esrd_qip'
    logger.info(f"Extracting from SQLServer {input_table.upper()} table "
                f"at {extract_conf['url']}")

    # Read unfiltered data from SQLServer
    input_df: DataFrame = spark.read\
        .format(extract_conf['format']) \
        .option('dbtable', input_table) \
        .option('url', extract_conf['url']) \
        .option('databaseName', extract_conf['databaseName']) \
        .option('driver', extract_conf['driver']) \
        .option('user', extract_conf['user']) \
        .option('password', extract_conf['password']) \
        .load()

    logger.debug(f'Read {input_df.count()} records')

    # TRANSFORM

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
    logger.debug(
        f"Loading MySQL {output_table.upper()} table at {load_conf['url']}")

    # Write the DataFrame to a new MySQL table
    output_df.write.format(load_conf['format']) \
             .option('dbtable', output_table) \
             .option('url', load_conf['url']) \
             .option('driver', load_conf['driver']) \
             .option('user', load_conf['user']) \
             .option('password', load_conf['password']) \
             .mode('overwrite') \
             .save()
    # default mode is 'create', which raises error if table exists
    # df.mode('append')  # add data to existing table
    # df.mode('overwrite')  # overwrite existing data

    logger.info('ETL process complete')


if __name__ == '__main__':
    main()
