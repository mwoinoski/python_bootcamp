from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("MinTemperatures")
sc = SparkContext(conf = conf)

def parseLine(line):
    fields = line.split(',')
    stationID = fields[0]
    entryType = fields[2]
    temperature = float(fields[3]) * 0.1 * (9.0 / 5.0) + 32.0
    return (stationID, entryType, temperature)

filepath: str = "file:///Users/Mike/Classes/Articulate Design/Sutter Health Python" + \
           "/FrankKanesTamingBigDatawithApacheSparkandPython_code/1800.csv"
results = sc.textFile(filepath) \
            .map(parseLine) \
            .filter(lambda x: "TMIN" in x[1]) \
            .map(lambda x: (x[0], x[2])) \
            .reduceByKey(lambda x, y: min(x,y)) \
            .collect()

for result in results:
    print(f"{result[0]}\t{result[1]:.2f}F")
