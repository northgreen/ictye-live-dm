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
#

import unittest
import sys
import os
import pytest

import pluginsystem
import depends


class connect_wrapper:
    def __init__(self, id, open):
        self.id = id
        self.open = open


# 初始化正确插件目录
@pytest.fixture
def currect_plugin_dir():
    test_confi = {'port': 12345, 'host': '127.0.0.1', 'index': './web/living room dm.html',
                  'websocket': {'port': 45466, 'path': '/websocket'},
                  'plugins': {'default_path': os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                           "test/test_plugin")},
                  'debug': 1,
                  'loglevel': 'DEBUG',
                  'logfile': {'open': 1,
                              'name': 'latest-log'}}

    pluginsystem.confi = test_confi
    yield pluginsystem.Plugin()
    pluginsystem.confi = None


# 初始化错误插件
@pytest.fixture
def no_main_plugin():
    test_confi = {'port': 12345,
                  'host': '000000000',
                  'index': './web/living room dm.html',
                  'websocket': {'port': 45466,
                                'path': '/websocket'},
                  'plugins': {'default_path': os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                           "test/test_no_main_error"),
                              },
                  'debug': 1,
                  'loglevel': 'DEBUG',
                  'logfile': {'open': 1,
                              'name': 'latest-log'}}

    pluginsystem.confi = test_confi
    yield pluginsystem
    pluginsystem.confi = None


@pytest.mark.asyncio
async def test_message_system(currect_plugin_dir):
    plugin = currect_plugin_dir
    async for i in plugin.get_plugin_message(params={"message": "message"}, connect=connect_wrapper(1, 1)):
        print(i)


# 测试消息分析器
def test_anaylazer(currect_plugin_dir):
    plugin = currect_plugin_dir
    plugin.message_analyzer({"message": "message"})


# 测试无主方法错误
def test_no_main_error(no_main_plugin):
    with pytest.raises(depends.plugin_errors.NoMainMather):
        plugin = pluginsystem.Plugin()
    assert True


# 🤔🤔🤔
if __name__ == '__main__':
    unittest.main()
