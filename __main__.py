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

if __name__ == "__main__":
    import logging
    from depends import logger, configs
    import http_server
    import pluginsystem
    import livewebsocket
    import asyncio
    import os
    import sys

    os.chdir(os.path.dirname(os.path.abspath(__file__)))


    async def message_loop():
        while True:
            msgs = await plugin_sys.get_plugin_message()
            if not msgs == []:
                logging.getLogger(__name__).debug(f"geting message {msgs}")
            livewebsocket.dm_dic.extend(msgs)
            await asyncio.sleep(2)


    def run_server():
        loop = asyncio.get_event_loop()
        loop.create_task(message_loop())
        loop.create_task(http_server.http_server(config))
        loop.create_task(livewebsocket.websocket_main(config))
        loop.create_task(plugin_sys.plugin_main_runner())
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass


    # 获取配置
    config = configs.config()
    # 传递配置
    http_server.config = config
    pluginsystem.confi = config
    livewebsocket.config = config
    # 获取插件系统
    plugin_sys = pluginsystem.Plugin()
    livewebsocket._plugin_system = plugin_sys
    http_server.plugin_system = plugin_sys
    # 获取logger
    logger.logging_setup(config)
    loggers = logging.getLogger(__name__)

    # 启动服务器
    loggers.info("project starting")
    loggers.info("金克拉，你有了吗？")
    run_server()

    loggers.info("project already stopped")

else:
    raise 0
