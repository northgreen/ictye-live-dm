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

from ....depends import plugin_main
import asyncio
import random


class Plugin_Main(plugin_main.Plugin_Main):
    def plugin_init(self):
        self.sprit_cgi_support = True
        self.sprit_cgi_path = "test"
        self.dm_list: list[dms] = []
        self.clock = True
        return "message"

    async def sprit_cgi(self, request):
        return self.web.Response(text="ok")

    async def plugin_main(self):
        while True:
            await asyncio.sleep(3)
            self.clock = not self.clock
            await asyncio.sleep(random.randint(1, 3))
            print("(^_^)")

    def plugin_callback(self):
        print(f"plugin {__name__} is done")

    def dm_iter(self, params, connect_id):
        # 生成一个dm对象
        if self.clock:
            return None
        dm = dms(fader_class=self, param=params)
        self.dm_list.append(dm)
        return dm


class dms:
    def __init__(self, fader_class: Plugin_Main, param: dict):
        self.param: dict = param
        self.fader_class = fader_class
        self.message_list = []

    def __aiter__(self):
        for msg in self.param.items():
            yield msg
