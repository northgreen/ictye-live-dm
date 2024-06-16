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
import asyncio

try_imp = True
import sys

sys.path.append("./")

import os
from urllib.parse import urlparse
from . import blivedm
from depends import pluginmain, msgs
import shutil

import aiohttp
from aiohttp import web
from typing import *
import http.cookies
from .blivedm.clients import ws_base
from .blivedm.models import web as web_models
import logging

logger = logging.getLogger(__name__)
local_path = __path__[0]


async def download_file(url, file_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(file_name, 'wb') as file:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    file.write(chunk)


async def return_for_face(path: str):
    if path:
        files = os.listdir(os.path.join(local_path, "tmp"))
        file = os.path.basename(urlparse(path).path)
        if file in files:
            return web.FileResponse(os.path.join(local_path, "tmp", file))
        else:
            await download_file(path, os.path.join(local_path, "tmp", file))
            return web.FileResponse(os.path.join(local_path, "tmp", file))


class Handler(blivedm.BaseHandler):
    def __init__(self, lists: list):
        self.user_face: dict = {}
        self.lists = lists

    def _on_danmaku(self, client: blivedm.BLiveClient, message):
        logger.info(f'[{client.room_id}] {message.uname}：{message.msg}')
        self.user_face[message.uname] = ""
        peop_type = {0: 0, 1: 1, 2: 2, 3: 3}
        message = msgs.msg_box(
            message_class="default",
            message_body=msgs.dm(
                msg=message.msg,
                who=msgs.msg_who(
                    type=peop_type[message.privilege_type] if message.admin == 0 else 5,
                    name=message.uname,
                    face="/cgi/b_dm_plugin/face?url=" + ""
                ).to_dict()
            ).to_dict(),
            msg_type="dm"
        ).to_dict()
        self.lists.append(message)

    def _on_gift(self, client: ws_base.WebSocketClientBase, message: web_models.GiftMessage):
        logger.info(f'[{client.room_id}] {message.uname} 赠送{message.gift_name}x{message.num}'
                    f' （{message.coin_type}瓜子x{message.total_coin}）')
        peop_type = {0: 0, 1: 1, 2: 2, 3: 3}
        message = msgs.msg_box(
            message_class="default",
            message_body=msgs.info(
                msg=f"感谢{message.uname}赠送的{message.gift_name}",
                who=msgs.msg_who(
                    type=peop_type[message.guard_level],
                    name=message.uname,
                    face="/cgi/b_dm_plugin/face?url=" + message.face
                ).to_dict(),
                pic=msgs.pic(
                    border=False,
                    pic_url="/cgi/b_dm_plugin/gift?item=" + message.gift_name + ".png"
                ).to_dict()
            ).to_dict(),
            msg_type="info"
        ).to_dict()
        self.lists.append(message)


# noinspection DuplicatedCode
class PluginMain(pluginmain.PluginMain):

    def plugin_init(self):
        if os.path.exists(os.path.join(local_path, "tmp")):
            shutil.rmtree(os.path.join(local_path, "tmp"))
            os.mkdir(os.path.join(local_path, "tmp"))
        else:
            os.mkdir(os.path.join(local_path, "tmp"))
        self.plugin_name = "b_dm_plugin"

        self.sprit_cgi_support = True
        self.sprit_cgi_lists["face"] = self.cgi_face
        self.sprit_cgi_lists["gift"] = self.cgi_gift
        self.read_config()

        # print(self.config)
        if "session" in self.config:
            self.SESSDATA = self.config["session"]
        else:
            self.config["session"] = ""
            self.update_config(self.config)

        return "message"

    async def cgi_face(self, request: web.Request):
        ret = web.Response(status=404, text="no such file")
        ret = await return_for_face(request.rel_url.query.get("url"))
        return ret

    async def cgi_gift(self, request: web.Request):
        return web.FileResponse(os.path.join(local_path, "resource", request.rel_url.query.get("item")))

    async def plugin_main(self):
        while True:
            await asyncio.sleep(1)

    def plugin_callback(self):
        logger.info(f"plugin {__name__} is done")

    def dm_iter(self, params: dict) -> object:
        class dm_iter_back:
            def __init__(self, params, session):
                self.messages = []
                if "broom" in params:
                    cookies = http.cookies.SimpleCookie()
                    cookies['SESSDATA'] = session
                    cookies['SESSDATA']['domain'] = 'bilibili.com'

                    self.session: Optional[aiohttp.ClientSession]
                    self.session = aiohttp.ClientSession()
                    self.session.cookie_jar.update_cookies(cookies)

                    self.client = blivedm.BLiveClient(params["broom"], session=self.session)

                    handler = Handler(self.messages)
                    self.client.set_handler(handler)
                    self.client.start()
                else:
                    logger.error("unexpected room, client will be invalid!")

            async def __aiter__(self):
                try:
                    yield self.messages.pop()
                except IndexError:
                    return

            async def callback(self):
                logger.info("blivedm closing")
                if hasattr(self, "client"):
                    await self.session.close()
                    await self.client.stop_and_close()

        return dm_iter_back(params, self.SESSDATA)
