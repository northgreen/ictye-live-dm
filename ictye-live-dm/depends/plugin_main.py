#  Copyright (c) 2023 楚天寻箫（ictye）
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

from . import plugin_errors, msgs
import asyncio
import typing
from . import configs as configs
from . import connects
from aiohttp import web


class Plugin_Main:

    @typing.final
    def __init__(self):
        """
        不要用这个而是用plugin_init来进行插件的初始化，这个仅供内部使用
        """
        self.stop: bool = False
        self.plugin_js_sprit_support: bool = False  # js插件支持
        self.plugin_js_sprit: str = ""  # js插件

        self.type: str = str()  # 插件类型

        self.config: dict = dict()  # 配置

        self.sprit_cgi_support = False  # 插件cgi支持

        self.sprit_cgi_lists: {} = {}  # cgi列表

        self.plugin_name: str = ""  # 插件名称

        self.web: web = web  # web模块

        if self.plugin_type() == "message":
            self.message_list = []

    def plugin_init(self) -> str:
        """
            插件开始被加载时调用
            父函数本身不实现任何功能
            需要返回插件类型给插件系统以判断插件类型
            (实际上这个类就是个异步迭代器)

            return:如果是”message“则表示这是个消息提供插件，如果是”analyzer“则表示这个插件是用来获取中间消息并且进行处理的。
        """
        self.stop = 0
        raise plugin_errors.UnexpectedPluginMessage('插件入口方法没有实现')

    async def plugin_main(self):
        """
        插件的主方法，此方法停止时插件也会被视为运行完毕
        """
        pass

    async def message_filter(self, message) -> msgs.msg_box:
        """

        消息过滤器,用于自动处理消息，比如翻译或者敏感词过滤
        :param message:待处理的消息
        :return 消息

        """
        return message

    async def message_anaylazer(self, message):

        """
        消息分析
        """

        pass

    async def sprit_cgi(self, request):
        """
        脚本cgi接口
        :param request:请求对象
        :return 响应，用aiohttp的就行（已经封装为self.web）
        """
        if self.sprit_cgi_support:
            raise plugin_errors.UnexpectedPluginMather("未实现的插件方法")

    def dm_iter(self, params: dict, connect_waper: connects.connect_wrapper) -> object:
        """
        返回弹幕迭代对象
        :param params: 前端的get参数
        :param connect_waper: 连接信息
        :return 消息迭代对象

        """
        return self

    @typing.final
    def update_config(self):
        """
        更新配置，将自身的配置写入文件并且保存在计算机上
        """
        assert self.plugin_name != ""
        configs.set_config(self.plugin_name, self.config)

    @typing.final
    def read_config(self):
        """
        读取配置
        """
        assert self.plugin_name != ""
        self.config = configs.read_config(self.plugin_name)

    def __aiter__(self):
        if self.plugin_type() == "message":
            return self

    async def __anext__(self):
        if self.plugin_type() == "message":
            if self.message_list:
                return self.message_list.pop(0)
            else:
                raise StopAsyncIteration()

    @typing.final
    def plugin_stop(self):
        """
        插件停止
        """
        self.stop = 1
        asyncio.current_task().cancel()

    def plugin_callback(self):

        """
        插件回调
        """

        print(f"plugin is done")

    @typing.final
    def plugin_getconfig(self) -> dict:
        """
        获取配置
        """
        return configs.config()

    @typing.final
    def plugin_type(self) -> str:
        """
        获取插件类型
        """
        # 不存在则初始化插件类型，并返回插件类型给软件以判断插件类型
        # 不存在插件类型则表示插件没有被加载，返回插件没有被加载的错误信息给软件以判断插件是否被加载
        if not self.type:
            self.type = self.plugin_init()
        return self.type
