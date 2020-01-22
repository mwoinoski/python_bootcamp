"""
Driver for an ETL process that extracts a CSV file and loads a CSV file.
"""

from etl_process import EtlProcess
from extractor import ExtractorCsv
from transformer import TransformerTopFiveCust
from loader import LoaderCsv
from etl_logger import EtlLogger


if __name__ == '__main__':
    logger = EtlLogger()
    logger.info('ETL Process starting')

    extract_file = 'customer-orders.csv'
    # path: str = f'file://{Path().absolute()}/{file}'  # read local file
    extract_path = f'hdfs://localhost:9000/user/sutter/data/{extract_file}'  # read from Hadoop server
    extractor = ExtractorCsv({'path': extract_path})

    transformer = TransformerTopFiveCust()

    load_path = './customer-orders-totals.csv'
    loader = LoaderCsv({'path': load_path})

    etl_process = EtlProcess(extractor, transformer, loader)
    etl_process.run()

    logger.info('ETL Process complete')
