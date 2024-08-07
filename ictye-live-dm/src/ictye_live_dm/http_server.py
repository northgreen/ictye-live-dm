import json
import logging
import os
import sys
from typing import Optional

from aiohttp import web

from . import livewebsocket
from . import pluginsystem
from .depends import configs

config: configs.ConfigManager = configs.ConfigManager()
plugin_system: pluginsystem.Plugin = pluginsystem.Plugin()
log = logging.getLogger(__name__)
runner: Optional[web.AppRunner] = None

def return_file(file: str):
    async def header(request):
        nonlocal file
        log.info("return for main_page")
        return web.FileResponse(path=file, status=200)

    return header


async def http_handler(request: web.Request):
    """
        主文件请求
    """
    return web.HTTPFound("/index")


async def http_socket_get(request: web.Request):
    log.info("return for socket")
    return web.Response(text=json.dumps({"code": 200, "local": "/ws"}))


async def http_websocket(request: web.Request):
    ws = "ws://{}:{}".format(config["host"], config["websocket"]["port"])
    return web.WebSocketResponse


async def http_plugin(request: web.Request):
    log.info(f"request for {request.match_info['name']}")
    if os.path.exists(f"web/js/plugin/{request.match_info['name']}"):
        return web.FileResponse(path=f"web/js/plugin/{request.match_info['name']}")
    elif request.match_info["name"] in plugin_system.plugin_js_support:
        return web.Response(text=plugin_system.plugin_js_support[request.match_info["name"]],
                            content_type="application/javascript")
    else:
        return web.Response(status=404, text="not found")


async def http_style(request: web.Request):
    log.info(f"request for {request.match_info['name']}")
    return web.FileResponse(path=f"web/style/{request.match_info['name']}")


async def http_js(request: web.Request):
    log.info(f"request for {request.match_info['name']}")
    return web.FileResponse(path=f"web/js/{request.match_info['name']}")


async def http_lib(request: web.Request):
    log.info(f"request for {request.match_info['name']}")
    return web.FileResponse(path=f"web/js/lib/{request.match_info['name']}")


async def http_script(request: web.Request):
    log.info(f"request for {request.match_info['name']}")
    return web.FileResponse(path=f"web/js/script/{request.match_info['name']}")


async def http_api_plugin(request: web.Request):
    log.info(f"request for web plugin list")

    plugin_list = {"code": 200,
                   "list": [os.path.splitext(file_name)[0] for file_name in os.listdir("web/js/plugin") if
                            file_name.endswith('.js')] + list(plugin_system.plugin_js_support)}

    return web.json_response(plugin_list)


async def http_cgi(request: web.Request):
    """
    HTTP ic py cgi前端调用
    """
    req = web.Response(status=404, text="not such path")
    try:
        if request.match_info["name"] in plugin_system.plugin_cgi_support:
            if request.match_info["page"] in plugin_system.plugin_cgi_support[request.match_info["name"]]:
                req = await plugin_system.plugin_cgi_support[request.match_info["name"]][request.match_info["page"]](
                    request)
            else:
                req = web.Response(status=404, text="no such path")
        else:
            req = web.Response(status=404, text="no such plugin")
    except Exception as e:
        log.error(f"cgi plugin error:{str(e)}")
        req = web.Response(status=504, text=f"cgi error :{str(e)}")
    return req


async def http_server():
    app = web.Application()

    route_list: [web.RouteDef] = [web.get("/", http_handler),
                                  web.get("/get_websocket", http_socket_get),
                                  web.get("/style/{name}", http_style),
                                  web.get("/js/plugin/{name}", http_plugin),
                                  web.get("/js/{name}", http_js),
                                  web.get("/js/lib/{name}", http_lib),
                                  web.get("/js/script/{name}", http_script),
                                  web.get("/ws", livewebsocket.aiohttp_ws),
                                  web.get("/api/plugin_list", http_api_plugin),
                                  web.get("/cgi/{name}/{page}", http_cgi)
                                  ]
    for k in config["web"]:
        file = list(k.keys())[0]
        route_list.append(web.get(f"/{file}", return_file(k.get(file).get())))

    app.add_routes(route_list)

    global runner
    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, config["host"], config["port"])
    # http服务器
    log.info("http server started")
    try:
        await site.start()
        log.info(f"server is starting at http://{config['host']}:{config['port']}")
    except OSError:
        log.fatal(f"port {config['port']} have been used!")
        sys.exit(1)
