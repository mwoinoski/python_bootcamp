from pyspark.sql import SparkSession, DataFrame
from util import file_url


# Create a SparkSession
spark: SparkSession = SparkSession.builder \
                                  .appName("SparkSQL")\
                                  .getOrCreate()

csv_schema: str = 'ID int, name string, age int, numFriends int'
df: DataFrame = spark.read.csv(path=file_url("fakefriends.csv"),
                               schema=csv_schema) \
                                    .cache()

# Register the DataFrame as a table.
df.createOrReplaceTempView("people")

# SQL can be run over DataFrames that have been registered as a table.
teenagers = spark.sql("SELECT * FROM people WHERE age >= 13 AND age <= 19")

# The results of SQL queries are RDDs and support all the normal RDD operations.
for teen in teenagers.collect():
    print(teen)

# We can also use functions instead of SQL queries:
teenagers.groupBy("age").count().orderBy("age").show()

spark.stop()
