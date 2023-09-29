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
