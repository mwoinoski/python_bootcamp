from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("PopularMovies")
sc = SparkContext(conf = conf)

file = "hdfs://localhost:9000/user/pydev/ml-100k/u.data"
lines = sc.textFile(file)
movies = lines.map(lambda x: (int(x.split()[1]), 1))
movieCounts = movies.reduceByKey(lambda x, y: x + y)

flipped = movieCounts.map(lambda x: (x[1], x[0]))
sortedMovies = flipped.sortByKey()

results = sortedMovies.collect()

for result in results:
    print(result)
