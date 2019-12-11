"""
Counts the number of occurrences of each movie rating 1-5
"""

from typing import Dict
from pyspark import SparkConf, SparkContext, RDD

# initialize spark
conf: SparkConf = SparkConf().setMaster("local").setAppName("RatingsHistogram")
sc: SparkContext = SparkContext(conf=conf)

# Here, our data is in the Hadoop distributed file system, but it could be
# a file:// URI for a local file or an s3a:// URI for an Amazon S3 bucket.

# The hadoop URI prefix is configured in $HADOOP_HOME/etc/hadoop/core-site.xml
filepath: str = "hdfs://localhost:9000/user/pydev/ml-100k/u.data"

# Read the file of movie ratings into an RDD (resilient distributed datastore).
lines: RDD = sc.textFile(filepath)

# extract the 3rd field from each record (the movie's rating from 1 to 5)
# into a new RDD
ratings: RDD = lines.map(lambda x: x.split()[2])

# count the occurrences of each rating and store the results in an dict.
# Each item's key is the rating. The item's value is the number of occurrences.
result: Dict[int, int] = ratings.countByValue()

# print the count for each rating
key: int
value: int
for key, value in sorted(result.items()):
    print(f"{key} {value}")
