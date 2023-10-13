import asyncio
import json
import msgs
from websockets import server
import logging
from depends import logger
import pluginsystem

dm_dic = []  # 弹幕列表
_plugin_system: pluginsystem.Plugin
config = {}
connects: list[server.WebSocketServerProtocol] = []
param_dict = {}


async def sub_dm_send():
    """
    弹幕总发送方法
    """
    logger.logging_setup(config)
    loggers = logging.getLogger()

    connect: server.WebSocketServerProtocol

    while True:
        for connect in connects:
            async for dms in dm(param_dict[connect.id] if connect.id in param_dict else {}):
                if connect.open:
                    mdm = await _plugin_system.message_filter(dms)  # 过滤消息
                    await _plugin_system.message_analyzer(mdm)  # 回调消息
                    loggers.info(f"sending message {mdm}")
                    await connect.send(json.dumps(mdm))  # 发送消息
                else:
                    asyncio.current_task().cancel()
                    try:
                        await asyncio.sleep(5)
                    except asyncio.CancelledError:
                        pass
        await asyncio.sleep(0.05)


class dm:
    """
    弹幕迭代器
        这个类是用来存储和读取弹幕信息的，
        使用 add_dm方法添加一条弹幕消息
        迭代此类可以获得弹幕信息，同时已经读取过的弹幕信息将会被弹出
    """

    def __init__(self, param):
        self.param = param
        pass

    def __aiter__(self):
        return self

    async def __anext__(self):
        while True:
            message = await _plugin_system.get_plugin_message(self.param)
            dm_dic.extend(message)
            try:
                return dm_dic.pop(0)
            except IndexError:
                await asyncio.sleep(1)

    def __contains__(self, item):
        return item in dm_dic


async def websockets(websocket: server.WebSocketServerProtocol):
    loggers = logging.getLogger(__name__)
    """
    websocket消息处理主函数
    """

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
                        param_dict[websocket.id] = ret["param"]
                        _plugin_system.socket_param[websocket.id] = ret["param"]

                    await websocket.send(json.dumps(msgs.connect_ok().to_dict()))
                    connects.append(websocket)  # 添加到链接列表

                    while websocket.open:
                        await asyncio.sleep(2)
                    pass

                else:
                    loggers.error("connect failed,unexpected client")
                    await websocket.close()

            except TypeError:
                loggers.warning("json decode failed")
    except asyncio.CancelledError:
        loggers.info("?i am canceled?")
    finally:
        await websocket.close()


async def websocket_main(configs):
    """
    websocket主函数，通过configs传递参数字典
    """

    logger.logging_setup(configs)
    loggers = logging.getLogger(__name__)
    loggers.info("websocket server started")

    await server.serve(websockets, configs["host"], configs["websocket"]["port"], logger=loggers)
    asyncio.get_event_loop().create_task(sub_dm_send())
