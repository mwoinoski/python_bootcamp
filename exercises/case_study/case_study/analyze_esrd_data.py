"""
Perform data analytics on Medicare ESRD data
"""

from typing import List
from pyspark.sql import SparkSession, DataFrame, Row
import pyspark.sql.functions as f


# sc = spark.sparkContext
# df = sc.parallelize([('Hosp A', '123'), ('Hosp B', '234'), ('Hosp C', '123')]).toDF().toDF('facility', 'ccn')

# initialize spark
spark: SparkSession = SparkSession.builder \
                                  .appName('ESRD QIP Data Analytics') \
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

# get a summary of the total performance scores
stats = ["count", "min", "20%", "40%", "60%", "80%", "max", "mean", "stddev"]
df.select(score).summary(*stats).show()

# get the high and low total performance score
tpf_max = df.agg(f.max(score)) \
            .head(1)[0][0]
tpf_min = df.agg(f.min(score)) \
            .head(1)[0][0]
# agg() creates a new DatatFrame with one Row, which has the result of the
# aggregate function
# head(1) return a List with one element, which the first Row of the DataFrame
# [0][0] gets the first element of the Row
# there are many ways to calculate the max or min of a row, but agg() seems
# to be the fastest. See https://stackoverflow.com/a/48776496/1313724
# agg() also accepts a dictionary of 'column name': 'function name'
print(f'Highest Total Performance Score: {tpf_max}')
print(f'Lowest Total Performance Score: {tpf_min}')
print()

# calculate the number of facilities that have each total performance score
# result_df = df_filtered.groupBy(score)\
#                        .count()\
#                        .orderBy(df_filtered[score].desc())

# Show lowest performing facilities

print(f'Facilities with lowest {score}')

result_df: DataFrame = df.select(name, state, score)\
                         .orderBy(df[score].asc())

result_df.show(n=10, truncate=False, vertical=True)


# MW TODO: PY2018 Payment Reduction Percentage ranges from 0.0% to 2.0%

# verify that values in column 'CMS Certification Number (CCN)' are unique

# MW TODO: good example for unit tests
ccn: str = 'CMS Certification Number (CCN)'
# we need a new DataFrame to refer to the 'count' column for the call to cast()
dupe_ccns: DataFrame = df.groupBy(df[ccn]) \
                         .count() \
                         .filter('count > 1')
dupes: int = dupe_ccns.count()
if dupes == 0:
    print(f"No facilities with duplicate {ccn}")
else:
    print(f"{dupes} facilities have a duplicate {ccn}:")
    dupe_ccns.show()
print()

# show facilities with highest Total Performance Score

print(f'Facilities with highest {score}')

max_tpf: float = df.select(f.max(score)).collect()[0][0]
# max_tpf = df_filtered.agg(F.max(score)).head(1)[0][0]  # same result
df.select(name, state, ccn, score) \
  .where(df_unfiltered[score] == max_tpf) \
  .show(n=100, truncate=False, vertical=True)

# calculate mean total performance of each state's dialysis center

result: List[Row] = df.selectExpr(f'`{state}` as state', f'`{score}` as score') \
                      .groupBy(f.col('state')) \
                      .agg(f.mean(f.col('score')).alias('avg'), f.count(f.col('score')).alias('num')) \
                      .sort('avg', ascending=False) \
                      .collect()

# We could run the same query as SQL
# df.selectExpr(f'`{state}` as state', f'`{score}` as score') \
#   .createOrReplaceTempView('state_score')
# query: str = f"""
#     select state, avg(score) as avg
#       from state_score
#      group by state
#      order by avg desc
# """
# result = spark.sql(query).collect()
#
# if column names contains spaces or other special characters, enclose them
# in backquotes `...`
# avg_col: str = 'Average TPS'
# query: str = f"""
#     select {state} as `State`, avg(`{score}`) as `{avg_col}`
#       from state_score
#      group by state
#      order by `{avg_col}` desc
# """

# show() doesn't support formatting options, so we'll resort to DIY
print(f'+----+-----+----------------+-----------+')
print(f'|Rank|State|Dialysis Centers|Average TPS|')
print(f'+----+-----+----------------+-----------+')
for i, row in enumerate(result):
    print(f'|{i:>4d}|{row.state:>5s}|{row.num:>16d}|{row.avg:>11.2f}|')
print(f'+----+-----+----------------+-----------+')


# MW TODO: measure mean performance by dialysis center owner

# MW TODO: look at a different measure than TPS


# result: List[Row] = df.toDF('cust_id', 'order_id', 'amount') \
#                       .select('cust_id', 'amount') \
#                       .groupBy('cust_id') \
#                       .agg(f.sum('amount').alias('total')) \
#                       .orderBy('total') \
#                       .collect()
#
# for row in result:
#     print(f'{row.cust_id} {row.total:.2f}')
