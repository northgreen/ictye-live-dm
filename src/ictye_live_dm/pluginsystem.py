#  Copyright (c) 2023-2024 楚天寻箫（ictye）
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

import asyncio
from .depends import pluginmain, plugin_errors
import logging
import os
import importlib
import importlib.util
import aiohttp.web as web

config = {}  # 配置


class Plugin:
    def __init__(self):
        mlogger = logging.getLogger(__name__)

        self.logger = mlogger

        self.message_plugin_list: list = []  # 消息插件列表
        self.analyzer_plugin_list: list = []  # 分析插件列表
        self.plugin_cgi_support: dict = {}  # 消息插件cgi
        self.plugin_js_support: dict = {}  # js支持字典
        self.connect_id_dict_aiohttp = {}  # 连接id——消息对象，为了防止重复向插件申请迭代对象(aiohttp)

        # 加载默认插件目录
        self.__lod_init_plugin__()

    def __lod_init_plugin__(self):
        plugin_name = ""
        for plugin_file in os.listdir(os.path.join(os.path.dirname(__file__), "plugin")):
            try:
                # 排除一些非法的文件和缓存目录，还要同时保障能够加载软件包
                if os.path.splitext(plugin_file)[1] == ".py" or os.path.isdir(
                        os.path.join(os.path.join(os.path.dirname(__file__), "plugin"),
                                     plugin_file)) and not plugin_file == "__pycache__":

                    plugin_name = os.path.splitext(plugin_file)[0]
                    path_name = os.path.join(os.path.dirname(__file__), "plugin")

                    self.logger.info(f"found a plugin '{plugin_name}' in dir {path_name}")

                    plugin_module = importlib.import_module(f'.plugin.{plugin_name}', package=__package__)

                    # 合法性检查
                    if not hasattr(plugin_module, "PluginMain"):
                        raise plugin_errors.NoMainMather("函数未实现主方法或者主方法名称错误")

                    plugin_class = getattr(plugin_module, "PluginMain")
                    plugin_interface: pluginmain.PluginMain = plugin_class()

                    # 获取插件类型
                    if plugin_interface.plugin_type() == "message":
                        self.message_plugin_list.append(plugin_interface)
                    elif plugin_interface.plugin_type() == "analyzer":
                        self.analyzer_plugin_list.append(plugin_interface)
                    else:
                        raise plugin_errors.PluginTypeError("未知的插件类型，该不会是插件吃了金克拉了吧？")

                    # 注册脚本cgi接口
                    if plugin_interface.sprit_cgi_support:
                        self.plugin_cgi_support[plugin_interface.plugin_name] = plugin_interface.sprit_cgi_lists
                    # 注册插件js
                    if plugin_interface.plugin_js_sprit_support:
                        self.plugin_js_support[plugin_interface.plugin_name] = plugin_interface.plugin_js_sprit

            except IndexError as e:
                self.logger.error(f"failed to import plugin :\n{plugin_name} {str(e)}")

    async def remove_connect_in_id_dict_aiohttp(self, id):
        """
        当连接关闭时，移除连接
        :param id 连接id
        """
        for i in self.connect_id_dict_aiohttp[id]:
            if hasattr(i, "callback"):
                await i.callback()
        return self.connect_id_dict_aiohttp.pop(id, False)

    async def get_plugin_message_aiohttp(self, params, connect: web.WebSocketResponse):
        """
        弹幕对象迭代器，迭代对应参数的弹幕
        """
        if connect in self.connect_id_dict_aiohttp.keys():
            # 已经缓存消息迭代器
            for dm_iter in self.connect_id_dict_aiohttp[connect]:
                async for _dm in dm_iter:
                    self.logger.debug("get a dm:", _dm)
                    yield _dm
        else:
            # 获取未缓存的消息迭代器
            self.connect_id_dict_aiohttp[connect] = []
            for plugin in self.message_plugin_list:
                dm = plugin.dm_iter(params)
                if dm is None:
                    continue
                self.connect_id_dict_aiohttp[connect].append(dm)

                async for _dm in dm:
                    self.logger.debug("get a dm:", _dm)
                    yield _dm

    async def message_analyzer(self, message):
        # 消息分析插件
        for plugins in self.analyzer_plugin_list:
            plugins.message_anaylazer(message)

    async def message_filter(self, message) -> dict:
        """
        消息过滤方法
        :param message: 消息对象
        :return: 处理后的消息对象
        :rtype: Message_Object
        """
        message_filtered = message
        for plugins in self.analyzer_plugin_list:
            if not plugins:
                try:
                    plugins.message_filter(message_filtered)
                except Exception as e:
                    self.logger.error(f"a error is happened:{str(e)}")
        return message_filtered

    async def plugin_main_runner(self):
        """
        运行插件主方法
        """
        message_plugin = []
        anaylazer_tasks = []
        for plugin in self.analyzer_plugin_list:
            tsk = asyncio.get_event_loop().create_task(plugin.plugin_main())
            tsk.add_done_callback(lambda l: asyncio.ensure_future(self.analyzer_plugin_callback(plugin)))
            anaylazer_tasks.append(tsk)
        for plugin in self.message_plugin_list:
            tsk = asyncio.get_event_loop().create_task(plugin.plugin_main())
            tsk.add_done_callback(lambda l: asyncio.ensure_future(self.message_plugin_call_back(plugin)))
            message_plugin.append(tsk)

        while True:
            for tsk in message_plugin:
                if tsk.done():
                    message_plugin.remove(tsk)
            for tsk in anaylazer_tasks:
                if tsk.done():
                    anaylazer_tasks.remove(tsk)
            await asyncio.sleep(1)

    async def message_plugin_call_back(self, obj):
        try:
            obj.plugin_callback()
        except Exception as e:
            self.logger.error(f"a error is happened:{str(e)}")
        self.message_plugin_list.remove(obj)

    async def analyzer_plugin_callback(self, obj):
        try:
            obj.plugin_callback()
        except Exception as e:
            self.logger.error(f"a error is happened:{str(e)}")
        self.analyzer_plugin_list.remove(obj)
