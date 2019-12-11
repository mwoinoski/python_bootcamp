from pyspark import SparkConf, SparkContext
import util

conf = SparkConf().setMaster("local").setAppName("PopularHero")
sc = SparkContext(conf = conf)


def count_co_occurences(line):
    elements = line.split()
    return int(elements[0]), len(elements) - 1


def parse_names(line):
    fields = line.split('\"')
    return int(fields[0]), fields[1].encode("utf8")


names = sc.textFile(util.file_url("Marvel-names.txt"))
namesRdd = names.map(parse_names)

lines = sc.textFile(util.file_url("Marvel-graph.txt"))

pairings = lines.map(count_co_occurences)
totalFriendsByCharacter = pairings.reduceByKey(lambda x, y: x + y)
flipped = totalFriendsByCharacter.map(lambda x_y: (x_y[1], x_y[0]))

mostPopular = flipped.max()

mostPopularName = namesRdd.lookup(mostPopular[1])[0]

print(f"{mostPopularName} is the most popular superhero, with " +
      f"{mostPopular[0]} co-appearances.")
