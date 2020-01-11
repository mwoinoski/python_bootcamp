from pyspark.sql import SparkSession
from pyspark.sql import Row
import util


def mapper(line):
    fields = line.split(',')
    return Row(ID=int(fields[0]),
               name=str(fields[1].encode("utf-8")),
               age=int(fields[2]),
               numFriends=int(fields[3]))


# Create a SparkSession
spark = SparkSession.builder.appName("SparkSQL").getOrCreate()

lines = spark.read.textFile(util.file_url("fakefriends.csv"))
people = lines.map(mapper)

# Infer the schema, and register the DataFrame as a table.
df = spark.createDataFrame(people).cache()
df.createOrReplaceTempView("people")

# SQL can be run over DataFrames that have been registered as a table.
teenagers = spark.sql("SELECT * FROM people WHERE age >= 13 AND age <= 19")

# The results of SQL queries are RDDs and support all the normal RDD operations.
for teen in teenagers.collect():
    print(teen)

# We can also use functions instead of SQL queries:
df.groupBy("age").count().orderBy("age").show()

spark.stop()
