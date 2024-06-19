from websockets.server import WebSocketServerProtocol
import aiohttp.web as web


class connect_wrapper:
    """
    连接包装类
    """

    def __init__(self, connect: WebSocketServerProtocol):
        self.__connect__ = connect
        self.id = connect.id  # 连接id
        self.open = connect.open  # 连接状态

    def refresh(self):
        """
        刷新状态
        """
        self.id = self.__connect__.id
        self.open = self.__connect__.open
