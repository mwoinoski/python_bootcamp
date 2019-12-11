"""
Min temps of weather stations
"""

from pyspark import SparkConf, SparkContext, RDD
from collections import OrderedDict, defaultdict


def parse_line(line):
    fields = line.split(',')
    # return (age, numFriends)
    return fields[0], int(fields[3])


# initialize spark
conf: SparkConf = SparkConf().setMaster("local").setAppName("RatingsHistogram")
sc: SparkContext = SparkContext(conf = conf)

filepath: str = "file:///Users/Mike/Classes/Articulate Design/Sutter Health Python" + \
           "/FrankKanesTamingBigDatawithApacheSparkandPython_code/1800.csv"
lines: RDD = sc.textFile(filepath)
# extract the 3rd field from each record (the movie's rating from 1 to 5, with no fractional values)
mins = lines.filter(lambda x: 'TMIN' in x.split(',')[2]) \
             .map(parse_line) \
             .reduceByKey(lambda v1, v2: min_temp(v1, v2)) \
             .collect()   

# print the count for each rating
for station_id, min_temp in sorted(mins):
    print(f"{station_id} {min_temp}")
