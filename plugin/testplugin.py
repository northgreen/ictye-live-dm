import plugin_main
import msgs
import asyncio
import random


class Plugin_Main(plugin_main.Plugin_Main):
    def plugin_init(self):
        return "message"

    async def plugin_main(self):
        usrname_list = ["guest1", "guest2", "guest3"]
        loop = 10000
        while not loop == 0:

            loop = loop - 1
            await asyncio.sleep(10)
            print("已经产生一个消息")
            # TODO:更新消息接口
            self.message_list.append(msgs.msg(usr=usrname_list[random.randint(0, 3)]).to_dict())

    def plugin_callback(self):
        print(f"plugin {__name__} is done")
