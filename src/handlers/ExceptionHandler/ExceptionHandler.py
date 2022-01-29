import sys
import traceback
import logging

from constants.paths import LOGS_PATH


class ExceptionHandler:
    def log(self, exception: Exception):
        self.config_logging().info(traceback.format_exc())

    @staticmethod
    def config_logging():
        logger = logging.getLogger("exampleApp")
        logger.setLevel(logging.INFO)

        fh = logging.FileHandler(LOGS_PATH)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        return logger

    @staticmethod
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)
