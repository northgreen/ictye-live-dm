import argparse
import asyncio
import logging
import os

from . import http_server
from . import pluginsystem
from .depends import logger, configs

print("Copyright (c) 2024 ictye")
window = None


# NOTICE by ictye(2023-11-24):项目要尽可能简洁，轻量，因为主播的电脑在开了直播软件后剩余的资源很少，别问我是怎么知道的。
# 变量命名的时候要声明好类型，我不是很喜欢动态类型，虽然它没什么毛病，但我就是不喜欢。
# 类名称和方法名称要易懂，除了循环用的临时变量。
# 好的风格会更容易维护，风格不好的pr我不会批准，别问为啥。

def run_server(loop=asyncio.get_event_loop()):
    loop.create_task(http_server.http_server())
    loop.create_task(pluginsystem.Plugin().plugin_main_runner())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        exit(0)


def parse_args():
    ...
    # TODO: 解析參數


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # TODO:應把參數解析放到獨立的地方
    parse = argparse.ArgumentParser(description=""" 
    一个基于python实现的模块化弹幕姬框架\n
    如果沒有任何參數，將會正常啓動
    """)
    parse.add_argument('-u', '--unportable', action='store_true', help='非便携性启动')
    parse.add_argument("-cfg", "--config", default="", help='指定配置目錄')
    parse.add_argument('-i', '--install', action="append", default=[], help='安裝插件')
    parse.add_argument('-l', '--list', action="store_true", help='列出所有的插件')
    parse.add_argument('-g', '--gui', action="store_true", help='启动图形界面')
    args = parse.parse_args()

    unportable: bool = args.unportable
    """便携启动开关"""
    configdir: str = args.config
    """配置目錄"""
    install: list = args.install
    """安裝插件"""
    list: bool = args.list
    GUI: bool = args.gui
    """列出插件"""
    if install:
        print(install)
        exit(0)
    elif GUI:
        os.system("pythonw -m ictye_live_dm.GUI_main")
        exit(0)

    # 获取配置
    config = configs.ConfigManager()
    config.read_default(os.path.dirname(__file__) + "/config/system/config.yaml")
    if configdir:
        config.load_config(configdir)

    # 获取logger
    logger.setup_logging(unportable)
    loggers = logging.getLogger(__name__)
    loggers.info("金克拉，你有了吗？")
    # 启动服务器
    loggers.info("project starting")
    run_server(asyncio.get_event_loop())

    loggers.info("project already stopped")
