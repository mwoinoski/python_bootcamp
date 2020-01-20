"""
Loader class implementation.
"""

from typing import Dict, Any

from elt_process.data_frame import DataFrame


class Loader:
    """ Loader implements the "load" process of ETL """

    def __init__(self, config: Dict[str, Any]):
        self.path = config['path']

    def load(self, df: DataFrame):
        pass
