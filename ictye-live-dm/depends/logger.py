import logging
import time
import os


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

    logger = logging.getLogger()  # 获取全局logger
    logger.setLevel(level_dic[config["loglevel"]])  # 设置日志级别

    # 创建一个handler，用于写入日志文件
    if not os.path.exists('logs'):
        os.makedirs('logs')

    fh = logging.FileHandler(
        os.path.join('logs', config["logfile"]["name"] + time.strftime("%Y%m%d_%H%M%S",time.localtime()) + ".log"),
        encoding="utf-8")
    fh.setLevel(level_dic[config["loglevel"]])

    # 创建一个handler，用于将日志输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(level_dic[config["loglevel"]])

    # 定义handler的输出格式
    formatter = logging.Formatter("[%(asctime)s,%(name)s] %(levelname)s : %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    if config["logfile"]["open"]:
        logger.addHandler(fh)
    logger.addHandler(ch)
