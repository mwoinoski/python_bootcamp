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
import logging.config
from typing import Dict, Tuple
from pyspark.sql import SparkSession, DataFrame

input_table: str = 'esrd_qip'
output_table: str = 'esrd_qip_clean'

mode: str = 'prod'  # can be changed with a command line argument
config_file: str = 'config.ini'
logging_config_file: str = 'logging.ini'
logger_name: str = 'etl_demo'
logger: logging.Logger


def main():
    global input_table, output_table, config_file, mode, logger, \
        logging_config_file, logger_name

    args: Namespace = get_cmd_line_args(config_file)
    extract_conf, load_conf = get_extract_load_configs(args, config_file)

    logger.info('ETL process starting...')

    spark: SparkSession = initialize_spark_session()

    input_df: DataFrame = extract(extract_conf, input_table, spark)
    output_df: DataFrame = transform(input_df)
    load(load_conf, output_df, output_table)

    logger.info('ETL process complete')


def initialize_spark_session():
    spark: SparkSession = SparkSession.builder \
        .appName('ESRD QIP ETL Demmo') \
        .getOrCreate()
    return spark


def extract(config: Dict[str, str], table_name: str, spark: SparkSession) \
        -> DataFrame:
    global logger
    logger.info(f"Extracting from SQLServer {table_name.upper()} table "
                f"at {config['url']}")
    # Read unfiltered data from SQLServer
    input_df: DataFrame = spark.read \
        .format(config['format']) \
        .option('dbtable', table_name) \
        .option('url', config['url']) \
        .option('databaseName', config['databaseName']) \
        .option('driver', config['driver']) \
        .option('user', config['user']) \
        .option('password', config['password']) \
        .load()
    logger.debug(f'Read {input_df.count()} records')
    return input_df


def transform(input_df: DataFrame) -> DataFrame:
    for col in input_df.columns:
        new_name: str = normalize_column_name(col, 64)
        input_df = input_df.withColumnRenamed(col, new_name)
    # Another option:
    # renamed_cols = [f.col(c).alias(re.sub(r'\W', '_', c[:64].strip()))
    #                 for c in input_df.columns]
    # input_df = input_df.select(renamed_cols)

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


def load(config: Dict[str, str], output_df: DataFrame, table_name: str) \
        -> None:
    global logger
    logger.debug(
        f"Loading MySQL {table_name.upper()} table at {config['url']}")
    # Write the DataFrame to a new MySQL table
    output_df.write.format(config['format']) \
        .option('dbtable', table_name) \
        .option('url', config['url']) \
        .option('driver', config['driver']) \
        .option('user', config['user']) \
        .option('password', config['password']) \
        .mode('overwrite') \
        .save()
    # default mode is 'create', which raises error if table exists
    # df.mode('append')  # add data to existing table
    # df.mode('overwrite')  # overwrite existing data


def get_cmd_line_args(default_config_file: str) -> Namespace:
    global mode
    parser: ArgumentParser = ArgumentParser(description='Run ETL Process')
    help_msg: str = f'path to config file (defaults to {default_config_file})'
    parser.add_argument('-c', '--config-file', type=str, help=help_msg)
    parser.add_argument('-m', '--mode', type=str, help='dev, test, or prod')
    args: Namespace = parser.parse_args()
    # don't define a default value for the --mode argument: we need to know
    # if they set the mode explicitly
    if args.mode:
        mode = args.mode
    return args


def get_extract_load_configs(args: Namespace, default_config_file: str) \
        -> Tuple[Dict[str, str], Dict[str, str]]:
    # if --config-file is set, read that file.
    # otherwise, if --mode is set, read the file with the mode in the name.
    # otherwise, read the default file.
    conf_file: str = default_config_file
    if args.config_file:
        conf_file = args.config_file
    elif args.mode:
        name_ext = default_config_file.split('.')
        conf_file = f'{name_ext[0]}-{args.mode}.{name_ext[1]}'
    config: ConfigParser = ConfigParser()
    if not config.read(conf_file):
        raise Exception(f"couldn't read config file {conf_file}")
    return config['extract'], config['load']


if __name__ == '__main__':
    logging.config.fileConfig(logging_config_file)
    logger = logging.getLogger(logger_name)

    main()
