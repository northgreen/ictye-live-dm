import asyncio
import json
from websockets import server
import logging
from depends import msgs
import pluginsystem

plugin_system: pluginsystem.Plugin
config: dict = {}
param_list: dict = {}
connect_list: list[server.WebSocketServerProtocol] = []
loggers = logging.getLogger(__name__)


async def websockets(websocket: server.WebSocketServerProtocol):
    """
    websocket消息处理主函数
    """
    # 连接检测
    try:
        async for message in websocket:
            loggers.info("receive a message" + message)

            # 解码信息，注意信息必须是json格式
            ret = json.loads(message)
            if (ret["code"] == 200 and ret["msg"] == "ok") or websocket in connect_list:  # 连接验证
                loggers.info("connect with blower success")
                await websocket.send(json.dumps(msgs.connect_ok().to_dict()))

                # 分析参数，并保存参数信息
                if "param" in ret:
                    param_list[websocket.id] = ret["param"]
                    loggers.debug("param_list", param_list)

                # 发送弹幕
                while websocket.open:
                    await asyncio.sleep(0.5)
                    dms: dict
                    async for dms in plugin_system.get_plugin_message(ret["param"], websocket):
                        # 过滤消息，并分析消息
                        mdm = await plugin_system.message_filter(dms)
                        await plugin_system.message_analyzer(mdm)

                        loggers.debug(f"sending message {mdm}")

                        # 发送消息
                        await websocket.send(json.dumps(mdm))
            else:
                # 认证失败就关闭连接
                loggers.error("connect failed,unexpected client")
                await websocket.close()

    finally:
        # 后续的处理
        await websocket.close()
        await plugin_system.remove_connect_in_id_dict(websocket.id)


async def websocket_main(configs):
    """
    websocket主函数，通过configs传递参数字典
    """
    loggers.info("websocket server started")
    try:
        await server.serve(websockets, configs["host"], configs["websocket"]["port"])
    except Exception as e:
        loggers.error(f"websockets haven't started currently,because of {str(e)}")
