import asyncio
import json
import msgs
from websockets import server
import logging
from depends import logger
import pluginsystem


plugin_system: pluginsystem.Plugin
config = {}
param_list: dict = {}
connect_list: list[server.WebSocketServerProtocol] = []


async def sub_message_loop(test = False):
    logger.logging_setup(config)
    loggers = logging.getLogger(__name__)

    count = 10
    while True:
        if test:
            if count == 0:
                break
            count -= 1
        loggers.info("sub_message_loop")
        for connects in connect_list:
            dms: dict
            __dm = plugin_system.get_plugin_message(param_list[connects.id] if connects.id in param_list else [],connects)
            async for dms in __dm:
                if connects.open:
                    mdm = await plugin_system.message_filter(dms)
                    await plugin_system.message_analyzer(mdm)
                    loggers.info(f"sending message {mdm}")
                    await connects.send(json.dumps(mdm))
                else:
                    connect_list.remove(connects)
        await asyncio.sleep(0.5)


async def websockets(websocket: server.WebSocketServerProtocol):
    loggers = logging.getLogger(__name__)
    """
    websocket消息处理主函数
    """

    """
    连接检测
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
                        param_list[websocket.id] = ret["param"]
                        print("param_list", param_list)

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
