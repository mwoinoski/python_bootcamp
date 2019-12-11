"""
"""

from pyspark import SparkConf, SparkContext, RDD

def current_dir(filename: str) -> str:
    import pathlib
    parent = str(pathlib.Path().absolute()).replace('\\', '/')[2:]
    return f"file://{parent}/{filename}"

def parseLine(line):
    fields = line.split(',')
    return (fields[0], int(fields[3]))

# initialize spark
conf: SparkConf = SparkConf().setMaster("local").setAppName("PySparkApplication")
sc: SparkContext = SparkContext(conf = conf)

file = '1800.csv'
rdd: RDD = sc.textFile(current_dir(file))
# rdd: RDD = sc.parallelize([
#                 "ITE00100554,18000101,TMAX,-75,,,E,",
#                 "ITE00100554,18000101,TMIN,-148,,,E,",
#                 "EZE00100082,18000101,TMAX,-86,,,E,",
#                 "EZE00100082,18000101,TMIN,-135,,,E,"
#                 ])

result = rdd.filter(lambda x: 'TMIN' in x.split(',')[2]) \
            .map(parseLine) \
            .reduceByKey(lambda v1, v2: min(v1, v2)) \
            .collect()   

# print the count for each rating
for station_id, min in sorted(result):
    print(f"{station_id} {min/10:.1f}C")
