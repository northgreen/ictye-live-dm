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
from websockets.server import WebSocketServerProtocol


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

