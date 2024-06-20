import importlib
import logging
import os
import time

from . import configs
from . import gui_log_formatter
from . import gui_logging_hadler

config = configs.ConfigManager()


def setup_logging(unportable: bool, window=None):
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
        os.path.join(log_path, config["logfile"]["name"] + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + ".log"),
        encoding="utf-8")

    fh.setLevel(level_dic[config["loglevel"]])

    # 创建一个handler，用于将日志输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(level_dic[config["loglevel"]])

    # 定义handler的输出格式
    file_formatter = logging.Formatter("[%(asctime)s,%(name)s] %(levelname)s : %(message)s")
    if window:
        gh = logging.StreamHandler()
        gformatter = gui_log_formatter.GuiLogFormatter(window)
        gh.setLevel(level_dic[config["loglevel"]])
        gh.setFormatter(gformatter)
        logger.addHandler(gh)

        gh = gui_logging_hadler.GUI_Handler(window)
        gh.setLevel(level_dic[config["loglevel"]])
        # logger.addHandler(gh)

    try:
        formatter = importlib.import_module("colorlog").ColoredFormatter(
            "%(log_color)s[%(asctime)s,%(name)s]%(levelname)s\t%(blue)s%(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={},
            style='%'
        )
    except ModuleNotFoundError:
        formatter = logging.Formatter("[%(asctime)s,%(name)s] %(levelname)s : %(message)s")

    fh.setFormatter(file_formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    if config["logfile"]["open"]:
        logger.addHandler(fh)
    logger.addHandler(ch)

    tmp_logger = logging.getLogger(__name__)

    tmp_logger.info("log path " + log_path)
