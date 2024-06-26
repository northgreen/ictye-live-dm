import logging
import time
import os


def setup_logging(config: dict, unportable: bool):
    """
    Setup logging configuration
    """

    level_dic: dict = {"DEBUG": logging.DEBUG,
                       "INFO": logging.INFO,
                       "WARNING": logging.WARNING,
                       "ERROR": logging.ERROR,
                       "CRITICAL": logging.CRITICAL,
                       "FATAL": logging.FATAL}

    if unportable:
        appdata_path = os.getenv('APPDATA')
        log_path = os.path.join(appdata_path, "ictye_live_dm", "log")
    else:
        log_path = "logs"
    """日志档案路径"""

    logger = logging.getLogger()  # 获取全局logger
    logger.setLevel(level_dic[config["loglevel"]])  # 设置日志级别

    # 创建一个handler，用于写入日志文件
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    fh = logging.FileHandler(
        os.path.join(log_path, config["logfile"]["name"] + time.strftime("%Y%m%d_%H%M%S",time.localtime()) + ".log"),
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

    tmp_logger = logging.getLogger(__name__)

    tmp_logger.info("log path " + log_path)
