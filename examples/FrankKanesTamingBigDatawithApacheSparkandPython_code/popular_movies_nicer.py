"""
Demo of broadcasting an object to all Spark processing nodes
"""

from typing import Dict, List, TextIO, Tuple
import codecs
from operator import add
from pyspark import SparkConf, SparkContext, RDD, Broadcast
from pyspark.sql import Row


def load_movie_names() -> Dict[int, str]:  # ID, title
    """ Load move IDs and titles """
    movie_names: Dict[int, str] = {}
    file: TextIO
    with codecs.open("./ml-100k/u.item", encoding="cp1252") as file:
        line: str
        for line in file:
            fields: List[str] = line.split('|')
            movie_names[int(fields[0])] = fields[1]
    return movie_names


conf: SparkConf = SparkConf().setMaster("local").setAppName("PopularMovies")
sc: SparkContext = SparkContext(conf=conf)

name_dict_broadcast: Broadcast = sc.broadcast(load_movie_names())
# name_dict_broadcast.value is the Dict[id, title] returned by load_movie_names

filepath: str = "hdfs://localhost:9000/user/pydev/ml-100k/u.data"
lines: RDD = sc.textFile(filepath)
movies: RDD = lines.map(lambda x: (int(x.split()[1]), 1))  # (ID, 1)
movieCounts: RDD = movies.reduceByKey(add)  # (ID, count)

flipped: RDD = movieCounts.map(lambda id_count: (id_count[1], id_count[0]))
sortedMovies: RDD = flipped.sortByKey() # (count, ID) sorted ascending by count

# map sortedMovies to a new RDD with ()
sortedMoviesWithNames: RDD = sortedMovies.map(
    lambda count_id: (name_dict_broadcast.value[count_id[1]], count_id[0]))

results: List[Row] = sortedMoviesWithNames.collect()

result: Row
for result in results:
    print(result)
