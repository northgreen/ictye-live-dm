import os
import sys
import pytest
os.chdir("..")
import time

sys.path.append(os.path.split(os.path.abspath(__name__))[0].rsplit(os.sep, 0)[0])
import livewebsocket




def test_test():
    print("test test")
    assert True


# test sub_message_loop

@pytest.mark.asyncio
async def test_sub_message_loop():
    print("test sub_message_loop")
    await livewebsocket.sub_message_loop(test=True)
    assert True


def test_websocket_main():
    print("test websocket_connect")
    assert True
