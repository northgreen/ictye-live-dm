import plugin_erroers
import msgs
import asyncio


class Plugin_Main:

    def __init__(self):
        self.type = None
        self.stop = 0
        if self.plugin_type() == "message":
            self.message_list = []

    def plugin_init(self):
        """
            插件开始被加载时调用
            父函数本身不实现任何功能
            需要返回插件类型给插件系统以判断插件类型
            (实际上这个类就是个异步迭代器)

            return:如果是”message“则表示这是个消息提供插件，如果是”analyzer“则表示这个插件是用来获取中间消息并且进行处理的。
        """
        self.stop = 0
        raise plugin_erroers.UnexpactedPluginMessage('插件入口方法没有实现')

    async def plugin_main(self):
        # 插件名义上的主方法，会被调用，但是没有实际作用，此方法停止时插件也会被视为运行完毕
        pass

    def plugin_type(self):
        if not self.type:
            self.type = self.plugin_init()
        return self.type

    # 通过异步迭代器的方法，插件能向软件发送消息
    async def __anext__(self):
        if self.plugin_type() == "message":
            if self.message_list:
                return self.message_list.pop(0)
            else:
                raise StopAsyncIteration()

    def __aiter__(self):
        if self.plugin_type() == "message":
            return self

    async def message_loop(self, message):
        """
        插件获取消息消息回环，将会接受消息

        """
        if self.plugin_type() == "analyzer":
            raise plugin_erroers.UnexpactedPluginMessage("不符合插件类型的插件实现")

    async def message_filter(self, message):
        """
        消息过滤器
        用于自动处理消息，比如翻译或者敏感词过滤
        """
        return message

    def plugin_stop(self):
        asyncio.current_task().cancel()

    def plugin_callback(self):
        print(f"plugin is done")
