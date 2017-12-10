__author__ = 'omar'
import logging
from slack import SlackService

__author__ = 'omar'


class Logger:
    logger = None

    def __init__(self, name):
        self.logger = logging.getLogger(name=name)

    def get_logger(self):
        return self.logger

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def info(self, message):
        self.logger.info(message)

    def critical(self, message):
        self.logger.critical(message)

    def extreme_logging(self, message, severity='error'):
        """
        log message into the log file and slack as well

        :param message:
        :param severity:
        :return:
        """
        SlackService.simple_message(message)
        log_method = getattr(self, severity)
        log_method(message)
