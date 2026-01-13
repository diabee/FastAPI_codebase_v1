import os
from logging.handlers import TimedRotatingFileHandler
import logging


class LoggingConfig:
    _instance = None

    def __init__(self):
        if LoggingConfig._instance is not None:
            raise Exception("Only one instance can exist")
        else:
            formatter = logging.Formatter(
                "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] - %(message)s -"
            )
            logger = logging.getLogger("core-log")
            handler = TimedRotatingFileHandler(
                os.getenv("LOG_PATH"),
                when=os.getenv("LOG_ROTATE_WHEN", "D"),
                interval=int(os.getenv("LOG_ROTATE_INTERVAL", "1")),
                backupCount=int(os.getenv("LOG_BACKUP_COUNT", "180")),
                encoding="UTF-8",
                delay=False,
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            logging.getLogger("core-log").addHandler(console)
            logger.setLevel(os.getenv("LOG_LEVEL", "DEBUG"))
            LoggingConfig._instance = logger

    @staticmethod
    def get_logger():
        if LoggingConfig._instance is None:
            LoggingConfig()
        return LoggingConfig._instance
