"""
Calculate total spending by customer in customer-orders-without-header.csv
"""

from pyspark import SparkConf, SparkContext, RDD
from operator import add
from pathlib import Path


def parse_csv_record(line):
    fields = line.split(',')
    return int(fields[0]), float(fields[2])


# initialize spark
conf: SparkConf = SparkConf().setMaster("local").setAppName("TotalSpentByCustomer")
sc: SparkContext = SparkContext(conf=conf)

# Customer ID,Order ID,Order Total
# 44,8602,37.19
file: str = 'customer-orders.csv'
file_url: str = f'file://{Path().absolute()}/{file}'
print(f'\nReading customer spend data from {file_url}\n')

rdd: RDD = sc.textFile(file_url)
header = rdd.first()  # extract header row
rdd = rdd.filter(lambda row: row != header)  # remove header row

result = rdd.map(parse_csv_record) \
            .reduceByKey(add) \
            .sortBy(lambda key_value: key_value[1], ascending=False) \
            .take(5)

for cust_id, total in result:
    print(f"{cust_id} {total:.2f}")
