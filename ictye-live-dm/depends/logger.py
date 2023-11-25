import logging


def setup_logging(config: dict):
    """
    Setup logging configuration
    """

    level_dic: dict = {"DEBUG": logging.DEBUG,
                       "INFO": logging.INFO,
                       "WARNING": logging.WARNING,
                       "ERROR": logging.ERROR,
                       "CRITICAL": logging.CRITICAL,
                       "FATAL": logging.FATAL}
    logging.basicConfig(level=level_dic[config["loglevel"]], format="[%(asctime)s,%(name)s] %(levelname)s : %(message)s")
