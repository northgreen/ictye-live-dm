from aiohttp import web
import livewebsocket
import asyncio
import msgs
import json
import logging
from depends import logger, configs
import pluginsystem

confi = None


async def http_handler(request):  # 主文件请求
    log = logging.getLogger(__name__)
    log.info("return for mainpage")
    return web.FileResponse(path="web/living room dm.html", status=200)


async def http_socket(request):
    log = logging.getLogger(__name__)
    log.info("return for socket")
    return web.Response(text=json.dumps(msgs.socket_responce(confi).to_dict()))


async def http_server(configs):
    # http服务器

    print("http server started")

    app = web.Application()
    app.add_routes([web.get("/", http_handler), web.get("/websocket", http_socket)])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, configs["host"], configs["port"])
    await site.start()


async def message_loop():
    print("aaaaaa")
    while True:
        msgs = await livewebsocket.pluginsystem.get_plugin_message()
        livewebsocket.dm_dic.extend(msgs)
        await asyncio.sleep(5)


def run_server(configs):
    global confi
    confi = configs

    loop = asyncio.get_event_loop()
    loop.create_task(message_loop())
    loop.create_task(http_server(configs))
    loop.create_task(livewebsocket.websocket_main(configs))
    loop.create_task(livewebsocket.pluginsystem.plugin_main_runner())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


config = configs.config()
pluginsystem.confi = config

logger.logging_setup()
loggers = logging.getLogger(__name__)

loggers.info("project starting")
loggers.info("金克拉，你有了吗？")

livewebsocket.pluginsystem = pluginsystem.Plugin()

run_server(config)  # 运行服务器

loggers.info("project already stopped")
