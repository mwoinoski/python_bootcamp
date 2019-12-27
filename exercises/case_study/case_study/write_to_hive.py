"""
Perform data analytics on Medicare ESRD data and write results to a Hive table
"""

from typing import List
from pyspark.sql import SparkSession, DataFrame, Window
import pyspark.sql.functions as f


# initialize spark
spark: SparkSession = SparkSession.builder \
                                  .appName('ESRD QIP Data Analytics') \
                                  .enableHiveSupport() \
                                  .getOrCreate()

data_uri: str = 'hdfs://localhost:9000/user/sutter/data/'
file: str = 'ESRD_QIP-Complete_QIP_Data-Payment_Year_2018.csv'
df_unfiltered: DataFrame = spark.read.csv(data_uri + file,
                                          inferSchema=True, header=True)

# spark.read.csv(file, inferSchemna=True) will identify numeric columns if the
# column has no non-numeric values. In this case, some 'Total Performace Score'
# values are 'No Score', so the column is identified as a string type. We'll
# need to filter out the non-numeric values and then convert to integers.

score: str = 'Total Performance Score'
name: str = 'Facility Name'
state: str = 'State'
no_score: str = 'No Score'

print(f'Analyzing {df_unfiltered.count()} ESRD facilities')

# filter out facilities with no total performance score, and
# convert the score to an integer
df: DataFrame = \
    df_unfiltered.where(df_unfiltered[score] != no_score) \
                 .withColumn(score, df_unfiltered[score].cast('integer'))

# calculate mean total performance of each state's dialysis center
w: Window = Window.orderBy(f.desc('avg'))

mean_tps_df: DataFrame = \
    df.selectExpr(f'`{state}` as state', f'`{score}` as score') \
      .groupBy(f.col('state')) \
      .agg(f.mean(f.col('score')).alias('avg'), f.count(f.col('score')).alias('count')) \
      .withColumn('rank', f.row_number().over(w))
      # .sort('avg', ascending=False)

print('results from DataFrame:')
mean_tps_df.show(5)

# Write the DataFrame to a new Hive table
mean_tps_df.createOrReplaceTempView("rankings")
create_sql = """
    CREATE TABLE IF NOT EXISTS dialysis_center_ranking
    (rank INT, state String, count INT, avg_tps float)
"""
spark.sql(create_sql)
insert_sql = """
    insert into dialysis_center_ranking 
    select rank, state, count, avg from rankings
"""
spark.sql(insert_sql)

print('results from Hive DataFrame:')
hive_df: DataFrame = spark.sql("select * from dialysis_center_ranking") \
                          .show(5)
