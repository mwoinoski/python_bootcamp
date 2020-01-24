"""
Driver for an ETL process that extracts a CSV file and loads a CSV file.
"""

from case_study.etl.etl_process import EtlProcess
from case_study.etl.extractor_csv import ExtractorCsv
from case_study.etl.transformer_top_5 import TransformerTopFiveCust
from case_study.etl.loader_csv import LoaderCsv
from case_study.etl.etl_logger import EtlLogger


def main():
    logger = EtlLogger()
    logger.info('ETL Process starting')

    # Create Extractor
    extract_file = 'customer-orders.csv'
    # path: str = f'file://{Path().absolute()}/{file}'  # read local file
    extract_path = f'hdfs://localhost:9000/user/sutter/data/{extract_file}'  # read from Hadoop server
    extractor = ExtractorCsv({'path': extract_path})

    # Create Transformer
    transformer = TransformerTopFiveCust()

    # Create Loader
    load_path = './customer-orders-totals.csv'
    loader = LoaderCsv({'path': load_path})

    # Kick off the ETL process
    etl_process = EtlProcess(extractor, transformer, loader)
    etl_process.run()

    logger.info('ETL Process complete')


if __name__ == '__main__':
    main()
