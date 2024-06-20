import asyncio
import typing

from . import configs as configs
from . import plugin_errors, msgs


class PluginMain:

    def __init__(self):
        self.stop: bool = False
        """停止标志"""

        self.plugin_js_sprit_support: bool = False
        """js插件支持"""

        self.plugin_js_sprit: str = ""
        """js插件"""

        self.type: str = str()
        """插件类型"""

        self.config: dict = dict()
        """配置字典"""

        self.spirit_cgi_support = False
        """插件cgi支持"""

        self.sprit_cgi_lists: dict = dict()
        """cgi列表"""

        self.plugin_name: str = ""
        """插件名称"""

        if self.plugin_type() == "message":
            self.message_list = []

    def plugin_setup(self):
        """初始化插件"""
        pass

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

    async def message_analyzer(self, message):
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
        if self.spirit_cgi_support:
            raise plugin_errors.UnexpectedPluginMather("未实现的插件方法")

    def dm_iter(self, params: dict) -> object:
        """
        返回弹幕迭代对象
        :param params: 前端的get参数
        :return 消息迭代对象
        """
        return self

    @typing.final
    def update_config(self, config: dict):
        """
        更新配置，将自身的配置写入文件并且保存在计算机上
        """
        assert self.plugin_name != ""
        configs.set_config(self.plugin_name, config)

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
        return configs.ConfigManager()

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
