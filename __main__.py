if __name__ == "__main__":
    import logging
    from depends import logger, configs
    import http_server
    import pluginsystem
    import livewebsocket
    import asyncio


    async def message_loop():
        while True:
            msgs = await plugin_sys.get_plugin_message()
            livewebsocket.dm_dic.extend(msgs)
            await asyncio.sleep(5)

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
    #获取插件系统
    plugin_sys = pluginsystem.Plugin()
    #获取logger
    logger.logging_setup(config)
    loggers = logging.getLogger(__name__)

    #启动服务器
    loggers.info("project starting")
    loggers.info("金克拉，你有了吗？")
    run_server()

    loggers.info("project already stopped")

else:
    raise 0
