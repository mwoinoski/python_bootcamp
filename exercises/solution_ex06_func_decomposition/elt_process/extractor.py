"""
Extractor class implementation.
"""

from typing import Dict, Any

from elt_process.data_frame import DataFrame


class Extractor:
    """ Extractor implements the "extract" process of ETL """
    path: str

    def __init__(self, config: Dict[str, Any]):
        self.path = config['path']

    def extract(self) -> DataFrame:
        self.logger.info(f'Extract: {self.path}')

        return DataFrame()
