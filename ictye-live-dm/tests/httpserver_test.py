import pytest
import asyncio
from ictye_live_dm.http_server import *
from aiohttp import web

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
app.add_routes(route_list)


async def test_http(aiohttp_client, event_loop):
    client = await aiohttp_client(app)
    res = await client.get("/get_websocket")
    assert res.status == 200
    assert json.dumps({"code": 200, "local": "/ws"}) in await res.text()
