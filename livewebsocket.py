import asyncio
import json
import msgs
from websockets import server
import logging
from depends import logger

dm_dic = []  # 弹幕列表
connect_list = set()  # 连接合集
pluginsystem = None
config = {}

class dm:
    """
    弹幕迭代器
        这个类是用来存储和读取弹幕信息的，
        使用 add_dm方法添加一条弹幕消息
        迭代此类可以获得弹幕信息，同时已经读取过的弹幕信息将会被弹出
    """

    def __init__(self):
        pass

    def __aiter__(self):
        return self

    async def __anext__(self):
        while 1:
            try:
                return dm_dic.pop(0)
            except IndexError:
                await asyncio.sleep(1)

    def __contains__(self, item):
        return item in dm_dic


async def dm_send(socket):
    logger.logging_setup(config)
    loggers = logging.getLogger(__name__)

    loggers.info("socket connected,we will push dm to client")
    dmlist = dm()


    async for dms in dmlist:
        if not socket.closed:
            mdm = pluginsystem.Plugin.message_filter(dms)
            pluginsystem.Plugin.message_analyzer(mdm)
            loggers.info(f"sending message {mdm.to_dict()}")
            await socket.send(mdm.to_dict)
        else:
            asyncio.current_task().cancel()
            try:
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                pass


async def websockets(websocket):
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
    connect_list.add(websocket)

    conformed = 0  # 验证记录
    try:
        async for message in websocket:

            loggers.info("receive " + message)
            # 解码信息，注意信息必须是json格式
            try:
                ret = json.loads(message)
                if (ret["code"] == 200 and ret["msg"] == "ok") or conformed:  # 连接验证

                    loggers.info("connect with blower success")

                    # 开始推送发送弹幕
                    await websocket.send(json.dumps(msgs.connect_ok().to_dict()))
                    asyncio.get_running_loop().create_task(dm_send(websocket))

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
