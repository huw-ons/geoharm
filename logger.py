import logging
import datetime

FILE_NAME = "./{}/{}.log".format("logs", datetime.datetime.now().strftime(format="%Y-%m-%dT%H-%M-%S"))


def get_logger(name):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

        fileHandler = logging.FileHandler(FILE_NAME)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        fileHandler.setFormatter(formatter)

        logging.getLogger(name).addHandler(fileHandler)

    return logger
