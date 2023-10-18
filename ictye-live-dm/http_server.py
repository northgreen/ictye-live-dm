#  Copyright (c) 2023 楚天寻箫（ictye）
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

from aiohttp import web
import msgs
import json
import logging
import os
import pluginsystem

config = dict()
plugin_system: pluginsystem.Plugin


async def http_handler(request):  # 主文件请求
    log = logging.getLogger(__name__)
    log.info("return for main_page")
    return web.FileResponse(path="web/living room dm.html", status=200)


async def http_socket_get(request):
    log = logging.getLogger(__name__)
    log.info("return for socket")
    return web.Response(text=json.dumps(msgs.socket_responce(config).to_dict()))


async def http_websocket(request: web.Request):
    ws = "ws://{}:{}".format(config["host"], config["websocket"]["port"])
    return web.WebSocketResponse


async def http_plugin(request: web.Request):
    log = logging.getLogger(__name__)
    log.info(f"request for {request.match_info['name']}")
    if os.path.exists(f"web/js/plugin/{request.match_info['name']}"):
        return web.FileResponse(path=f"web/js/plugin/{request.match_info['name']}")
    elif request.match_info["name"] in plugin_system.plugin_js_support:
        return web.Response(text=plugin_system.plugin_js_support[request.match_info["name"]],
                            content_type="application/javascript")
    else:
        return web.Response(status=404, text="not found")


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


async def http_api_plugin(request):
    log = logging.getLogger(__name__)
    log.info(f"request for web plugin list")

    plugin_list = {"code": 200,
                   "list": [os.path.splitext(file_name)[0] for file_name in os.listdir("web/js/plugin") if
                            file_name.endswith('.js')] + list(plugin_system.plugin_js_support)}

    return web.json_response(plugin_list)


async def http_cgi(request):
    log = logging.getLogger(__name__)
    req = None
    try:
        if request.match_info["name"] in plugin_system.plugin_cgi_support:
            req = await plugin_system.plugin_cgi_support[request.match_info["name"]](request)
        else:
            req = web.Response(status=404, text="no such cgi")
    except Exception as e:
        log.error(f"cgi plugin error:{str(e)}")
        req = web.Response(status=404, text="no such cgi")
    return req


async def http_server(configs):
    # http服务器
    log = logging.getLogger(__name__)
    log.info("http server started")

    app = web.Application()
    app.add_routes([web.get("/", http_handler),
                    web.get("/get_websocket", http_socket_get),
                    web.get("/style/{name}", http_style),
                    web.get("/js/plugin/{name}", http_plugin),
                    web.get("/js/{name}", http_js),
                    web.get("/js/lib/{name}", http_lib),
                    web.get("/js/script/{name}", http_script),
                    web.get("/websocket", http_websocket),
                    web.get("/api/plugin_list", http_api_plugin),
                    web.get("/cgi/{name}", http_cgi)
                    ])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, configs["host"], configs["port"])
    await site.start()
