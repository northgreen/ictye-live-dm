import asyncio
import json
from websockets import server
import logging
from depends import logger, msgs
import pluginsystem

plugin_system: pluginsystem.Plugin
config: dict = {}
param_list: dict = {}
connect_list: list[server.WebSocketServerProtocol] = []


# TODO(ictye):这段逻辑在更改了消息插件的运行方式后显得好多余，并且消息推送存在强烈的顺序和阻塞，这不是我想要的。
#  或许未来（也许就是明天）我能把sub_message_loop改造或者移除掉。

async def sub_message_loop(test=False):
    logger.logging_setup(config)
    loggers = logging.getLogger(__name__)

    count = 10
    while True:

        # 测试用
        if test:
            if count == 0:
                break
            count -= 1

        for connects in connect_list:
            dms: dict
            __dm = plugin_system.get_plugin_message(param_list[connects.id] if connects.id in param_list else [],
                                                    connects)
            async for dms in __dm:
                if connects.open:
                    mdm = await plugin_system.message_filter(dms)
                    await plugin_system.message_analyzer(mdm)
                    loggers.info(f"sending message {mdm}")
                    await connects.send(json.dumps(mdm))
                else:
                    connect_list.remove(connects)
        await asyncio.sleep(0.1)


async def websockets(websocket: server.WebSocketServerProtocol):
    """
    websocket消息处理主函数
    """
    loggers = logging.getLogger(__name__)
    # 连接检测

    try:
        async for message in websocket:

            loggers.info("receive " + message)
            # 解码信息，注意信息必须是json格式
            try:
                ret = json.loads(message)
                if (ret["code"] == 200 and ret["msg"] == "ok") or websocket in connect_list:  # 连接验证

                    loggers.info("connect with blower success")

                    if "param" in ret:
                        param_list[websocket.id] = ret["param"]
                        loggers.debug("param_list", param_list)

                    await websocket.send(json.dumps(msgs.connect_ok().to_dict()))
                    connect_list.append(websocket)

                    await websocket.wait_closed()

                else:
                    loggers.error("connect failed,unexpected client")
                    await websocket.close()
            except TypeError:
                loggers.warning("json decode failed")
    finally:
        await websocket.close()
        connect_list.remove(websocket)
        plugin_system.remove_connect_in_id_dict(websocket.id)
        param_list.pop(websocket.id)


async def websocket_main(configs):
    """
    websocket主函数，通过configs传递参数字典
    """

    logger.logging_setup(configs)
    loggers = logging.getLogger(__name__)
    loggers.info("websocket server started")
    await server.serve(websockets, configs["host"], configs["websocket"]["port"])
    asyncio.get_running_loop().create_task(sub_message_loop())
