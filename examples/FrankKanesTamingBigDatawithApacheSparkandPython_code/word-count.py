from pyspark import SparkConf, SparkContext
from pathlib import Path

conf = SparkConf().setMaster("local").setAppName("WordCount")
sc = SparkContext(conf = conf)

file = 'book.txt'

parent = str(Path().absolute()).replace('\\', '/')[2:]
filepath = f"file://{parent}/{file}"

word_counts = sc.textFile(filepath) \
                .flatMap(lambda x: x.split()) \
                .countByValue()  # count of each unique value as (value, count) pairs

for word, count in sorted(word_counts.items(), key=lambda i: i[1], reverse=True):
    cleanWord = word.encode('ascii', 'ignore')
    if (cleanWord):
        print(cleanWord.decode() + " " + str(count))
