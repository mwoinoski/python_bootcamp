"""
Calculate total spending by customer in customer-orders.csv
"""

from pyspark import SparkConf, SparkContext, RDD
from operator import add
import util

def parseLine(line):
    fields = line.split(',')
    return int(fields[0]), float(fields[2])

# initialize spark
conf: SparkConf = SparkConf().setMaster("local").setAppName("TotalSpentByCustomer")
sc: SparkContext = SparkContext(conf = conf)

file = 'customer-orders.csv'
rdd: RDD = sc.textFile(util.file_url(file))

# This won't work with a CSV file that has a header. If you try something like
# this:
#   header = rdd.first()
#   rdd.filter(lambda line: line != header).map(...)
# Spark complains about a broken socket,
# For CSV with header(s), use a DataFrame instead

result = rdd.map(parseLine) \
            .reduceByKey(add) \
            .sortBy(lambda x: x[1]) \
            .collect()   

for cust_id, total in result:
    print(f"{cust_id} {total:.2f}")
