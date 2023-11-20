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
                    await websocket.send(json.dumps(msgs.connect_ok().to_dict()))
                    if "param" in ret:
                        param_list[websocket.id] = ret["param"]
                        loggers.debug("param_list", param_list)

                    # 发送弹幕

                    while websocket.open:
                        await asyncio.sleep(0.5)
                        dms: dict
                        __dm = plugin_system.get_plugin_message(ret["param"], websocket)
                        async for dms in __dm:
                            mdm = await plugin_system.message_filter(dms)
                            await plugin_system.message_analyzer(mdm)
                            loggers.info(f"sending message {mdm}")
                            await websocket.send(json.dumps(mdm))
                else:
                    loggers.error("connect failed,unexpected client")
                    await websocket.close()
            except TypeError:
                loggers.warning("json decode failed")
    finally:
        await websocket.close()
        plugin_system.remove_connect_in_id_dict(websocket.id)


async def websocket_main(configs):
    """
    websocket主函数，通过configs传递参数字典
    """

    logger.setup_logging(configs)
    loggers = logging.getLogger(__name__)
    loggers.info("websocket server started")
    await server.serve(websockets, configs["host"], configs["websocket"]["port"])
