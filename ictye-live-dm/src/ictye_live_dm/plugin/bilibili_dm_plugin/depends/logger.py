#  Copyright (c) 2024 楚天寻箫（ictye）
#
#    此软件基于楚天寻箫非商业开源软件许可协议 1.0发布.
#    您可以根据该协议的规定，在非商业或商业环境中使用、分发和引用此软件.
#    惟分发此软件副本时，您不得以商业方式获利，并且不得限制用户获取该应用副本的体验.
#    如果您修改或者引用了此软件，请按协议规定发布您的修改源码.
#
#    此软件由版权所有者提供，没有明确的技术支持承诺，使用此软件和源码造成的任何损失，
#    版权所有者概不负责。如需技术支持，请联系版权所有者或社区获取最新版本。
#
#   更多详情请参阅许可协议文档

import logging
import os
import time


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
