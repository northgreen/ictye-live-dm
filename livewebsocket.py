import asyncio
import json
import msgs
from websockets import server
import logging
from depends import logger
import pluginsystem

dm_dic = []  # 弹幕列表
plugin_system: pluginsystem.Plugin
config = {}
param_list: dict = {}
connect_list: list[server.WebSocketServerProtocol] = []


async def sub_message_loop():
    logger.logging_setup(config)
    loggers = logging.getLogger(__name__)

    loggers.info("socket connected,we will push dm to client")
    while True:
        for connects in connect_list:
            async for dms in dm(param_list[connects.id] if connects.id in param_list else []):
                if connects.open:
                    mdm = await plugin_system.message_filter(dms)
                    await plugin_system.message_analyzer(mdm)
                    loggers.info(f"sending message {mdm}")
                    await connects.send(json.dumps(mdm))
                else:
                    try:
                        await asyncio.sleep(5)
                    except asyncio.CancelledError:
                        pass
        await asyncio.sleep(0.5)


class dm:
    """
    弹幕迭代器
        这个类是用来存储和读取弹幕信息的，
        使用 add_dm方法添加一条弹幕消息
        迭代此类可以获得弹幕信息，同时已经读取过的弹幕信息将会被弹出
    """

    def __init__(self, param):
        self.param = param

    def __aiter__(self):
        return self

    async def __anext__(self):
        while True:
            dms = await plugin_system.get_plugin_message(self.param)
            dm_dic.extend(dms)
            try:
                return dm_dic.pop(0)
            except IndexError:
                break
                # FIXME

    def __contains__(self, item):
        return item in dm_dic


async def websockets(websocket: server.WebSocketServerProtocol):
    loggers = logging.getLogger(__name__)
    """
    websocket消息处理主函数
    """

    """
    连接检测
    """
    if websocket in connect_list:
        print("a same connect!")
        return
    connect_list.append(websocket)

    conformed = 0  # 验证记录
    try:
        async for message in websocket:

            loggers.info("receive " + message)
            # 解码信息，注意信息必须是json格式
            try:
                ret = json.loads(message)
                if (ret["code"] == 200 and ret["msg"] == "ok") or conformed:  # 连接验证

                    loggers.info("connect with blower success")

                    if "param" in ret:
                        param_list[websocket.id] = ret["param"]

                    await websocket.send(json.dumps(msgs.connect_ok().to_dict()))
                    connect_list.append(websocket)

                    while websocket.open:
                        await asyncio.sleep(0.05)

                else:
                    loggers.error("connect failed,unexpected client")
                    await websocket.close()
            except TypeError:
                loggers.warning("json decode failed")
    except asyncio.CancelledError:
        loggers.info("?i am canceled?")
    finally:
        await websocket.close()
        connect_list.remove(websocket)


async def websocket_main(configs):
    """
    websocket主函数，通过configs传递参数字典
    """

    logger.logging_setup(configs)
    loggers = logging.getLogger(__name__)
    loggers.info("websocket server started")
    await server.serve(websockets, configs["host"], configs["websocket"]["port"])
    asyncio.get_running_loop().create_task(sub_message_loop())
