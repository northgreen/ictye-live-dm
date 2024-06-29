import argparse
import asyncio
import logging
import os
import sys
import traceback

from . import GUI_main
from . import http_server
from . import pluginsystem
from .depends import logger, configs

# NOTICE by ictye(2023-11-24):项目要尽可能简洁，轻量，因为主播的电脑在开了直播软件后剩余的资源很少，别问我是怎么知道的。
# 变量命名的时候要声明好类型，我不是很喜欢动态类型，虽然它没什么毛病，但我就是不喜欢。
# 类名称和方法名称要易懂，除了循环用的临时变量。
# 好的风格会更容易维护，风格不好的pr我不会批准，别问为啥。

is_copyright_print = False
if not is_copyright_print:
    print("GPL 2024 ictye")
    is_copyright_print = True
window = None


def custom_excepthook(exc_type, exc_value, exc_traceback):
    sys.stderr.write("Oh my god, an error!\n")
    java_style_error = f"Error: {exc_type.__name__}: {exc_value}\n"

    # 格式化堆棧信息
    stack_trace = traceback.extract_tb(exc_traceback)
    for frame in stack_trace:
        filename, line_number, function_name, line_of_code = frame
        java_style_error += f"    at: {function_name} ({filename}:{line_number})\n"
    sys.stderr.write(java_style_error)


sys.excepthook = custom_excepthook


def loop_exception_handler(loop, context):
    if type(context["exception"]) is SystemExit:
        loop.stop()
        return
    sys.excepthook(type(context["exception"]), context["exception"], context["exception"].__traceback__)


def run_server(loop=asyncio.get_event_loop(), callback=None):
    loop.set_exception_handler(loop_exception_handler)
    ser = loop.create_task(http_server.http_server())
    loop.create_task(pluginsystem.Plugin().plugin_main_runner())
    try:
        loop.run_forever()
        loop.run_until_complete(http_server.runner.cleanup())
        if callback:
            callback()
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Thanks for using ictye_live_dm, see you next time!")
        exit(0)


def parse_args():
    parse = argparse.ArgumentParser(description="一個模塊化的彈幕姬框架")
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
    _list: bool = args.list
    gui: bool = args.gui

    # 获取配置
    config = configs.ConfigManager()
    config.read_default(os.path.dirname(__file__) + "/config/system/config.yaml")
    config.set("GUI", gui)

    if configdir:
        config.load_config(configdir)
    if install:
        print(install)
        exit(0)
    elif _list:
        print("\033[33mName\033[0m", "\t", "Description")
        for plugin in pluginsystem.Plugin().list_plugin():
            print("\033[33m" + plugin[0] + "\033[0m", "\t", plugin[1])
        exit(0)


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # 保證在正確的目錄下工作

    parse_args()  # 參數解析

    # 檢查GUI啓動
    if configs.ConfigManager()["GUI"]:
        print("starting gui")
        GUI_main.main()
        exit(0)

    # 获取logger
    logger.setup_logging()
    loggers = logging.getLogger(__name__)

    loggers.info("金克拉，你有了吗？")  # 代碼摻了金克拉，一行能當兩行寫（？）
    loggers.info("project starting")

    run_server(asyncio.get_event_loop())  # 启动服务器

    loggers.info("project already stopped")
