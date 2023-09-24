import json

import plugin_main
import msgs
import asyncio
import random


class Plugin_Main(plugin_main.Plugin_Main):
    def plugin_init(self):
        return "message"

    async def plugin_main(self):
        def create_user():
            usrname_list = ["guest1", "guest2", "guest3"]
            usericon_list = ["ico1", "ico2", "ico3"]
            return msgs.msg_who(random.randint(1, 6), usrname_list[random.randint(0, 2)],
                                usericon_list[random.randint(0, 2)]).to_dict()

        def create_dm():
            message_list = ["一转九五三六", "好哎", "挖，主播好卡哇伊", "恭喜恭喜"]
            return msgs.dm(message_list[random.randint(0, 3)],
                           create_user()).to_dict()

        def create_info():
            pass

        loop = 1000
        while not loop == 0:
            loop = loop - 1
            print("已经产生一个消息")
            # if random.randint(0,1) == 0:
            if True:
                msg = msgs.msg_box("default", "dm", create_dm()).to_dict()
            else:
                create_info()
            self.message_list.append(msg)
            await asyncio.sleep(10)

    def plugin_callback(self):
        print(f"plugin {__name__} is done")
