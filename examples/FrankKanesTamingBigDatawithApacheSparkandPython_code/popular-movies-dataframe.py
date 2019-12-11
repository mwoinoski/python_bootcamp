from pyspark.sql import SparkSession
from pyspark.sql import Row
from typing import List, Dict, TextIO
import codecs


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


spark = SparkSession.builder \
            .appName("PopularMovies") \
            .getOrCreate()

# Load up our movie ID -> name dictionary
name_dict = load_movie_names()

# Get the raw data
filepath: str = "hdfs://localhost:9000/user/pydev/ml-100k/u.data"
lines = spark.sparkContext.textFile(filepath)
# Convert it to a RDD of Row objects
movies = lines.map(lambda x: Row(movieID=int(x.split()[1])))
# Convert that to a DataFrame
movie_dataframe = spark.createDataFrame(movies)

# Some SQL-style magic to sort all movies by popularity in one line!
top_movie_ids = movie_dataframe.groupBy("movieID") \
                   .count() \
                   .orderBy("count", ascending=False) \
                   .cache()

# Show the results at this point:

# |movieID|count|
# +-------+-----+
# |     50|  584|
# |    258|  509|
# |    100|  508|

top_movie_ids.show()

# Grab the top 10
top10 = top_movie_ids.take(10)

# Print the results
print("\n")
for result in top10:
    # Each row has movieID, count as above.
    print(f"{name_dict[result[0]]} {result[1]}")

# Stop the session
spark.stop()
