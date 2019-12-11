"""
Better word count with sorting
"""

import re
from pyspark import SparkConf, SparkContext

def current_dir(filename: str) -> str:
    import pathlib
    parent = str(pathlib.Path().absolute()).replace('\\', '/')[2:]
    return f"file://{parent}/{filename}"

conf = SparkConf().setMaster("local").setAppName("WordCount")
sc = SparkContext(conf = conf)

input = sc.textFile(current_dir("book.txt"))

splitter_re = re.compile(r'\W+', re.UNICODE)

results = input.flatMap(lambda x: splitter_re.split(x.lower())) \
               .map(lambda word: (word, 1)) \
               .reduceByKey(lambda count1, count2: count1 + count2) \
               .map(lambda word_count: (word_count[1], word_count[0])) \
               .sortByKey() \
               .collect()

for result in results:
    word = result[1].encode('ascii', 'ignore')
    if (word):
        print(f"{word.decode()+':':12s}{result[0]:6d}")
