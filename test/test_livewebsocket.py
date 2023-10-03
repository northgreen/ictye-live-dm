# FIXME:此文件使用的接口已不适用
import os
import sys
import json

sys.path.append(os.path.split(os.path.abspath(__name__))[0].rsplit(os.sep, 0)[0])
import livewebsocket


def test_dm_list():
    print("testing livedm")

    tyl = [("jz", "1234513153", "4545455"), ("td", "23333333333", "233333333")]
    dmlist = livewebsocket.dm()

    for mag in tyl:
        dmlist.add_dm(type=mag[0], msg=mag[1], user=mag[2])

    def serialize_message(msg):
        return {
            "type": msg.msg,
            "msg": msg.usr,
            "user": msg.who
        }

    print(json.dumps(serialize_message(next(dmlist))))

    inn = 0
    expect = 1

    while expect == 1:
        print("inn:" + str(inn))
        try:
            print(json.dumps(serialize_message(next(dmlist))))
        except StopIteration:
            print("stop")
            break


def test_test():
    print("test test")
    assert True
