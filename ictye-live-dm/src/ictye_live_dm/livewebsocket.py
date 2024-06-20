import asyncio
import json
import logging

import aiohttp
from aiohttp import web

from . import pluginsystem
from .depends import msgs, configs

plugin_system: pluginsystem.Plugin = pluginsystem.Plugin()
config: configs.ConfigManager = configs.ConfigManager()
param_list: dict = {}
loggers = logging.getLogger(__name__)


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
            if ret["code"] == 200 and ret["msg"] == "ok":  # 连接验证
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
