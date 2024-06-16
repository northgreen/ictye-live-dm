#  Copyright (c) 2024 楚天寻箫（ictye）
#
#    此软件基于楚天寻箫非商业开源软件许可协议 1.0发布.
#    您可以根据该协议的规定，在非商业或商业环境中使用、分发和引用此软件.
#    惟分发此软件副本时，您不得以商业方式获利，并且不得限制用户获取该应用副本的体验.
#    如果您修改或者引用了此软件，请按协议规定发布您的修改源码.
#
#    此软件由版权所有者提供，没有明确的技术支持承诺，使用此软件和源码造成的任何损失，
#    版权所有者概不负责。如需技术支持，请联系版权所有者或社区获取最新版本。
#
#   更多详情请参阅许可协议文档

import asyncio
import json
from websockets import server
import logging
from .depends import msgs
from . import pluginsystem
from aiohttp import web
import aiohttp

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


async def aiohttp_ws(request: web.Request):
    """
    aiohttp ws處理程序
    """

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # 连接检测
    try:
        message: aiohttp.WSMessage
        async for message in ws:
            loggers.info("receive a message" + message.data)

            # 解码信息，注意信息必须是json格式
            ret = json.loads(message.data)
            if (ret["code"] == 200 and ret["msg"] == "ok") or ws in connect_list:  # 连接验证
                loggers.info("connect with blower success")
                await ws.send_str(json.dumps(msgs.connect_ok().to_dict()))

                await asyncio.sleep(0.5)
                dms: dict

                while 1:
                    await asyncio.sleep(0.5)
                    async for dms in plugin_system.get_plugin_message_aiohttp(ret["param"], ws):
                        # 过滤消息，并分析消息
                        mdm = await plugin_system.message_filter(dms)
                        await plugin_system.message_analyzer(mdm)

                        loggers.debug(f"sending message {mdm}")

                        # 发送消息
                        await ws.send_str(json.dumps(mdm))


            else:
                # 认证失败就关闭连接
                loggers.error("connect failed,unexpected client")
                await ws.close()

    finally:
        # 后续的处理
        await ws.close()
        await plugin_system.remove_connect_in_id_dict_aiohttp(ws)
    return ws


async def websocket_main(configs):
    """
    websocket主函数，通过configs传递参数字典
    """
    loggers.info("websocket server started")
    try:
        await server.serve(websockets, configs["host"], configs["websocket"]["port"])
    except Exception as e:
        loggers.error(f"websockets haven't started currently,because of {str(e)}")
