"""
Simple wrapper for logging.Logger
"""

import logging.config


class EtlLogger:
    """ Simple wrapper for logging.Logger """
    logging_config_file: str = 'logging.ini'
    logger_name: str = 'etl_process'
    logger: logging.Logger

    def __init__(self) -> None:
        """ Initialize the Logger """
        logging.config.fileConfig(self.logging_config_file,
                                  disable_existing_loggers=False)
        self.logger = logging.getLogger(self.logger_name)

    def critical(self, msg: str):
        self.logger.critical(msg)

    def debug(self, msg: str):
        self.logger.debug(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def fatal(self, msg: str):
        self.logger.fatal(msg)

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)
