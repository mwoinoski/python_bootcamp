"""
Counts the number of occurrences of each movie rating 1-5
"""

from typing import Dict
from pyspark import SparkConf, SparkContext, RDD

# initialize spark
conf: SparkConf = SparkConf().setMaster("local").setAppName("Most Popular Movie")
sc: SparkContext = SparkContext(conf=conf)

filepath: str = "hdfs://localhost:9000/user/pydev/ml-100k/u.data"
lines: RDD = sc.textFile(filepath)

result: Dict[int, int] = lines.map(lambda x: x.split()[1]).countByValue()
id, ratings = max(result.items(), key=lambda x: x[1])

file = "hdfs://localhost:9000/user/pydev/ml-100k/u.item"
title = sc.textFile(file) \
          .filter(lambda x: x.split('|')[0] == id) \
          .first() \
          .split('|')[1]
print(f"most popular movie: '{title}' with {ratings} ratings")
