from pyspark import SparkConf, SparkContext, RDD
from typing import List, Tuple

conf = SparkConf().setMaster("local").setAppName("FriendsByAge")
sc = SparkContext(conf = conf)

def parseLine(line):
    fields = line.split(',')
    # return (age, numFriends)
    return (int(fields[2]), int(fields[3]))

filepath: str = "file:///Users/Mike/Classes/Articulate Design/Sutter Health Python" + \
           "/FrankKanesTamingBigDatawithApacheSparkandPython_code/fakefriends.csv"
# read input lines: id, name, age, numFriends
lines: RDD = sc.textFile(filepath)

# map to an RDD whose items are key/value pairs, where key is age and value is numFriends.
# we get key+value instead of single values because parseLine returns a tuple
rdd: RDD = lines.map(parseLine)
# without a separate function, it gets ugly because lambdas can't contain an assignment:
# rdd: RDD = lines.map(lambda v: (int(v.split(',')[2]), int(v.split(',')[3])))

# map each numFriends value to a tuple (numFriends, 1), then sum and count.
# RDD.mapValues(): only the values are passed to the lambda, and the values are
# replaced by the result of the lambda; the RDD's keys are untouched.
# RDD.reduceByKey(): for each key, gather all values and perform the reduce operation;
# in this case, replace the old value with a tuple of the total number of friends
# and the total number of users with that age.
# RDD.mapValues(): replace the value tuple with the average number of friends for
# the given age.
# RDD.collect(): convert the RDD into a list of tuples.
results: List[Tuple[int, float]] = \
    rdd.mapValues(lambda value: (value, 1)) \
       .reduceByKey(lambda v1, v2: (v1[0] + v2[0], v1[1] + 1)) \
       .mapValues(lambda x: x[0] / x[1]) \
       .collect()

for age, average_friends in sorted(results):
    print(f"{age}:{average_friends:5.0f}")
