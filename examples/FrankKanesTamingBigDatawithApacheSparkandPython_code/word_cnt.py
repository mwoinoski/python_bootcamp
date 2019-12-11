"""
Spark's "Hello world": file word count
"""

from pyspark import SparkConf, SparkContext, RDD
from pathlib import Path

# initialize spark
conf: SparkConf = SparkConf().setMaster("local").setAppName("MyWordCount")
sc: SparkContext = SparkContext(conf = conf)

file = 'book.txt'

parent = str(Path().absolute()).replace('\\', '/')[2:]
filepath = f"file://{parent}/{file}"

word_count = sc.textFile(filepath) \
               .flatMap(lambda x: x.split()) \
               .count()   

print(f"book has {word_count} words")
