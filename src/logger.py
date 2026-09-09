import logging
import os

from src.config import LOG_DIR


def get_logger(name):

    logger = logging.getLogger(name)

    logger.setLevel(
        logging.INFO
    )


    if logger.handlers:

        return logger


    log_file = os.path.join(
        LOG_DIR,
        "app.log"
    )


    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - "
        "%(levelname)s - %(message)s"
    )


    file_handler = logging.FileHandler(
        log_file
    )

    file_handler.setFormatter(
        formatter
    )


    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter
    )


    logger.addHandler(
        file_handler
    )

    logger.addHandler(
        console_handler
    )


    return logger