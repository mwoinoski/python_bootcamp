from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("MinTemperatures")
sc = SparkContext(conf = conf)


def parse_line(line):
    fields = line.split(',')
    station_id = fields[0]
    entry_type = fields[2]
    temperature = float(fields[3]) * 0.1 * (9.0 / 5.0) + 32.0
    return station_id, entry_type, temperature


filepath: str = "file:///Users/Mike/Classes/Articulate Design/Sutter Health Python" + \
           "/FrankKanesTamingBigDatawithApacheSparkandPython_code/1800.csv"
results = sc.textFile(filepath) \
            .map(parse_line) \
            .filter(lambda x: "TMAX" in x[1]) \
            .map(lambda x: (x[0], x[2])) \
            .reduceByKey(lambda x, y: max(x,y)) \
            .collect()

for result in results:
    print(f"{result[0]}\t{result[1]:.2f}F")
