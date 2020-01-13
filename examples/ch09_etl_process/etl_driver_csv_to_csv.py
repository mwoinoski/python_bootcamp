"""
Driver for an ETL process that extracts a CSV file and loads a CSV file.
"""

from pathlib import Path

from etl_process import EtlProcess
from extractor import ExtractorCsv
from transformer import TransformerTopFiveCust
from loader import LoaderCsv
from etl_logger import EtlLogger

if __name__ == '__main__':
    logger = EtlLogger()
    logger.info('ETL Process starting')

    path: str = f'file://{Path().absolute()}/customer-orders.csv'  # read local file
    # path = f'hdfs://user/sutter/data/{file}'  # read from Hadoop server
    extractor = ExtractorCsv({'path': path})

    transformer = TransformerTopFiveCust()

    path = './customer-orders-totals.csv'
    loader = LoaderCsv({'path': path})

    etl_process = EtlProcess(extractor, transformer, loader)
    etl_process.run()

    logger.info('ETL Process complete')
