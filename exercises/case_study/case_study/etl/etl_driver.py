"""
Driver for an ETL process that extracts a CSV file and loads a CSV file.
"""

from pathlib import Path

from case_study.etl.etl_process import EtlProcess
from case_study.etl.extract.extractor_csv import ExtractorCsv
from case_study.etl.transform.transformer_clean_qip_data import TransformerCleanQipData
from case_study.etl.load.loader_csv import LoaderCsv
from case_study.etl.etl_logger import EtlLogger


def main():
    logger = EtlLogger()
    try:
        logger.info('ETL Process starting')

        # Create Extractor
        extract_file = 'ESRD_QIP-Complete_QIP_Data-Payment_Year_2018.csv'
        extract_path: str = f'file://{Path().absolute()}/data/{extract_file}'  # read local file
        # extract_path = f'hdfs://localhost:9000/user/sutter/data/{extract_file}'  # read from Hadoop server
        extractor = ExtractorCsv({'path': extract_path})

        # Create Transformer
        transformer = TransformerCleanQipData()

        # Create Loader
        load_path = './customer-orders-totals.csv'
        loader = LoaderCsv({'path': load_path})

        # Kick off the ETL process
        etl_process = EtlProcess(extractor, transformer, loader)
        etl_process.run()

        logger.info('ETL Process complete')
    except Exception as ex:
        logger.error(f'ETL Process error: {ex}')
        raise ex


if __name__ == '__main__':
    main()
