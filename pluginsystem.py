import asyncio
from depends import logger
import logging
import os
import importlib
import plugin_erroers
import importlib.util

confi = {}  # 配置


class Plugin:
    def __init__(self):

        mlogger = logging.getLogger(__name__)

        self.message_plugin_list: list = []
        self.analyzer_plugin_list: list = []
        self.plugin_cgi_support: dict = {}

        plugin_name = ""
        # 加载默认插件目录
        for plugin_file in os.listdir(confi['plugins']['default_path']):
            try:
                if os.path.splitext(plugin_file)[1] == ".py" or os.path.isdir(os.path.join(confi['plugins']['default_path'],plugin_file)) and not plugin_file == "__pycache__":
                    plugin_name = os.path.splitext(plugin_file)[0]
                    pathname = os.path.basename(confi['plugins']['default_path'])

                    mlogger.info(f"found a plugin '{plugin_name}' in {pathname}")

                    plugin_module = importlib.import_module(f'{pathname}.{plugin_name}')
                    plugin_class = getattr(plugin_module, "Plugin_Main")
                    plugin_interface = plugin_class()

                    # 获取插件类型
                    if plugin_interface.plugin_type() == "message":
                        self.message_plugin_list.append(plugin_interface)
                    elif plugin_interface.plugin_type() == "analyzer":
                        self.analyzer_plugin_list.append(plugin_interface)
                    else:
                        raise plugin_erroers.PluginTypeError("未知的插件类型，该不会是插件吃了金克拉了吧？")

                    # 注册脚本cgi接口
                    if plugin_interface.sprit_cgi_support:
                        self.plugin_cgi_support[plugin_interface.sprit_cgi_path] = plugin_interface.sprit_cgi
            except IndexError as e:
                mlogger.error(f"failed to import plugin :\n{plugin_name} {str(e)}")

        # 导入额外插件
        for plugin_file in confi["plugins"]["others_plugin"]:
            plugin_name = plugin_file
            try:
                if plugin_file is not None:
                    mlogger.info(f"loading plugin{plugin_file}")
                    path = os.path.normpath(plugin_file)
                    spec = importlib.util.spec_from_file_location(os.path.basename(path), os.path.dirname(path))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    plugin_main_class = module.Plugin_Main

                    # 获取插件类型
                    if plugin_main_class.plugin_type() == "message":
                        self.message_plugin_list.append(plugin_main_class)
                    elif plugin_main_class.plugin_type() == "analyzer":
                        self.analyzer_plugin_list.append(plugin_main_class)
                    else:
                        raise plugin_erroers.PluginTypeError("未知的插件类型，该不会是插件吃了金克拉了吧？")

                    # 注册插件cgi
                    if plugin_main_class.sprit_cgi_support:
                        if plugin_main_class.sprit_cgi_path:
                            self.plugin_cgi_support[plugin_main_class.sprit_cgi_path] = plugin_main_class.sprit_cgi
                        else:
                            raise
            except ImportError as e:
                mlogger.error(f"failed to import plugin {plugin_name:{str(e)}}")

    async def get_plugin_message(self):
        # 消息提取回环
        message_list = []
        for plugin in self.message_plugin_list:
            async for messages in plugin:
                message_list.append(messages)
        return message_list

    async def message_analyzer(self, message):
        # 漫游消息映射插件
        for plugins in self.analyzer_plugin_list:
            plugins.message_loop(message)

    async def message_filter(self, message):
        """
        消息过滤方法
        """
        mlogger = logging.getLogger(__name__)
        # 消息过滤
        message_filtered = message
        for plugins in self.analyzer_plugin_list:
            if not plugins:
                try:
                    plugins.message_filter(message_filtered)
                except Exception as e:
                    mlogger.error(f"a error is happened:{str(e)}")
        return message_filtered

    async def plugin_main_runner(self):
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
        obj.plugin_callback()
        self.message_plugin_list.remove(obj)

    async def analyzer_plugin_callback(self, obj):
        obj.plugin_callback()
        self.analyzer_plugin_list.remove(obj)


logger.logging_setup(confi)
