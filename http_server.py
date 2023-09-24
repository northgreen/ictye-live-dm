from aiohttp import web
import msgs
import json
import logging

config = None


async def http_handler(request):  # 主文件请求
    log = logging.getLogger(__name__)
    log.info("return for mainpage")
    return web.FileResponse(path="web/living room dm.html", status=200)


async def http_socket_get(request):
    log = logging.getLogger(__name__)
    log.info("return for socket")
    return web.Response(text=json.dumps(msgs.socket_responce(config).to_dict()))


async def http_websocket(request):
    ws = "ws://{}:{}".format(config["host"], config["websocket"]["port"])
    return web.WebSocketResponse


async def http_plugin(request):
    log = logging.getLogger(__name__)
    log.info(f"request for {request.match_info['name']}")
    return web.FileResponse(path=f"web/js/plugin/{request.match_info['name']}")


async def http_style(request):
    log = logging.getLogger(__name__)
    log.info(f"request for {request.match_info['name']}")
    return web.FileResponse(path=f"web/style/{request.match_info['name']}")


async def http_js(request):
    log = logging.getLogger(__name__)
    log.info(f"request for {request.match_info['name']}")
    return web.FileResponse(path=f"web/js/{request.match_info['name']}")


async def http_lib(request):
    log = logging.getLogger(__name__)
    log.info(f"request for {request.match_info['name']}")
    return web.FileResponse(path=f"web/js/lib/{request.match_info['name']}")


async def http_script(request):
    log = logging.getLogger(__name__)
    log.info(f"request for {request.match_info['name']}")
    return web.FileResponse(path=f"web/js/script/{request.match_info['name']}")


async def http_server(configs):
    # http服务器
    log = logging.getLogger(__name__)
    log.info("http server started")

    app = web.Application()
    app.add_routes([web.get("/", http_handler),
                    web.get("/get_websocket", http_socket_get),
                    web.get("/js/plugin/{name}", http_plugin),
                    web.get("/style/{name}", http_style),
                    web.get("/js/{name}", http_js),
                    web.get("/js/lib/{name}", http_lib),
                    web.get("/js/script/{name}", http_script),
                    web.get("/websocket", http_websocket)
                    ])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, configs["host"], configs["port"])
    await site.start()
