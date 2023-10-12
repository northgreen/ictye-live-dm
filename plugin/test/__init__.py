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

import json

import plugin_main
import msgs
import asyncio
import random


class Plugin_Main(plugin_main.Plugin_Main):
    def plugin_init(self):
        self.sprit_cgi_support = True
        self.sprit_cgi_path = "test"
        return "message"

    async def sprit_cgi(self, request):
        return self.web.Response(text="ok")

    async def plugin_main(self):
        def create_user():
            usrname_list = ["guest1", "guest2", "guest3"]
            usericon_list = ["ico1", "ico2", "ico3"]
            return msgs.msg_who(random.randint(0, 6), usrname_list[random.randint(0, 2)],
                                usericon_list[random.randint(0, 2)]).to_dict()

        def create_dm():
            message_list = ["一转九五三六", "好哎", "挖，主播好卡哇伊", "恭喜恭喜"]
            return msgs.dm(random.choice(message_list),
                           create_user()).to_dict()

        def create_info():
            message_list = ["一转九五三六", "好哎", "挖，主播好卡哇伊", "恭喜恭喜"]
            pic = ["a", "b", "c"]
            return msgs.info(random.choice(message_list),
                             create_user(),
                             msgs.pic(random.choice([True, False]),
                                      random.choice(pic)).to_dict()
                             ).to_dict()

        loop = 1000
        while not loop == 0:
            loop = loop - 1
            print("已经产生一个消息")
            if random.choice([True, False]):
                print("msg")
                msg = msgs.msg_box("default", "dm", create_dm()).to_dict()
            else:
                print("info")
                msg = msgs.msg_box("default", "info", create_info()).to_dict()
            self.message_list.append(msg)
            await asyncio.sleep(3)

    def plugin_callback(self):
        print(f"plugin {__name__} is done")
