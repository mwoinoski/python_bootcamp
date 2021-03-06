"""
Perform data analytics on Medicare ESRD data
"""
from typing import List, Set, Dict
from pyspark.sql import SparkSession, DataFrame, Column
import pyspark.sql.functions as f
from case_study import util


def normalize_name(name: str) -> str:
    return name.lower().replace(' ', '_')


data_files: List[str] = [
    'hvbp_tps_11_07_2017.csv',
    'hvbp_clinical_care_11_07_2017.csv',
    'hvbp_safety_11_07_2017.csv',
    'hvbp_efficiency_11_07_2017.csv',
    'hvbp_hcahps_11_07_2017.csv',
]

# initialize spark
spark: SparkSession = SparkSession.builder \
                                  .appName('Hospital Data Analytics') \
                                  .getOrCreate()

dfs: Dict[str, DataFrame] = {}
data_uri: str = 'hdfs://localhost:9000/user/sutter/data/'
for file in data_files:
    df = spark.read.csv(data_uri + file, inferSchema=True, header=True)
    col_aliases = [f.col(col_name).alias(normalize_name(col_name))
                   for col_name, col_type in df.dtypes]
    # col_names_normalized = [f.col(c).alias(normalize_name(c))
    #                         for c in col_aliases]
    dfs[file] = df.select(*col_aliases)

for k, v in dfs.items():
    print(f'{k} - Number of rows: {v.count()}, Number of columns: '
          f'{len(v.columns)}')

key_col: str = 'provider_number'

df_joined: DataFrame = dfs[data_files[0]]
# changes to df_master won't affect the original DataFrame

for i in range(1, len(data_files)):
    file = data_files[i]
    # use Set difference operator to eliminate duplicate columns
    cols_to_select: Set[str] = \
        set((key_col,)) | set(dfs[file].columns) - set(df_joined.columns)
    df_to_join = dfs[file].select(*cols_to_select)
    print(f'adding {len(df_to_join.columns)} columns from {file}\n')
    df_joined = df_joined.join(df_to_join, on=key_col, how='left')

print(f'final joined DF has {len(df_joined.columns)} columns: '
      f'{df_joined.columns}\n')
