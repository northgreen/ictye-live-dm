#  Copyright (c) 2024 楚天寻箫（ictye）
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

class PluginTypeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UnexpectedPluginMessage(Exception):
    def __init__(self, message):
        super(UnexpectedPluginMessage, self).__init__(message)


class UnexpectedPluginMather(Exception):
    def __init__(self, message):
        super(UnexpectedPluginMather, self).__init__(message)


class NoMainMather(Exception):
    def __init__(self, message):
        super(NoMainMather, self).__init__(message)
