"""
这个文件内定义全部的标准消息模板

所有的函数都应该又to_dict方法来将其转为字典，相反的这个函数能输出打包好的字典
别问我为啥，问就是不知道
"""


class datas:
    def to_dict(self, cls: object):
        return dict(cls)


class connect_ok:
    """
    连接认证消息
    """
    code = 200
    msg = "connect ok"

    def to_dict(self):
        return {"code": self.code,
                "msg": self.msg}


class dm:
    def __init__(self, msg: str, who: dict):
        """
        params:
        msg:str 消息主体
        who:dict 消息发出者对象（其实是一个字典）

        成员方法：
        to_dict: 输出为字典
        """
        self.msg = msg
        self.who = who

    def to_dict(self):
        return {"msg": self.msg,
                "who": self.who}


class info:
    def __init__(self,
                 msg: str,
                 who: str,
                 pic: dict):
        self.msg = msg
        self.who = who
        self.pic = pic

    def to_dict(self):
        return {"msg": self.msg,
                "who": self.who,
                "pic": self.pic}


class socket_responce:
    def __init__(self, config: dict):
        self.code = 200
        self.local = "ws://{}:{}".format(config["host"], config["websocket"]["port"])

    def to_dict(self):
        return {"code": self.code,
                "local": self.local}


class msg_who:
    def __init__(self, type: int,
                 name: str,
                 face: str):
        self.type = type
        self.name = name
        self.face = face

    def to_dict(self):
        return {"name": self.name,
                "type": self.type,
                "face": self.face}


class pic:
    def __init__(self,
                 border: bool,
                 pic_url: str):
        self.border = border
        self.pic_url = pic_url

    def to_dict(self):
        return {"border": self.border,
                "pic_url": self.pic_url}


class msg_box:
    """
    消息标准封装所用的类
    """

    def __init__(self,
                 message_class: str,
                 msg_type: str,
                 message_body: dict):
        self.message_class = message_class
        self.msg_type = msg_type
        self.message_body = message_body

    def to_dict(self):
        return {"message_class": self.message_class,
                "msg_type": self.msg_type,
                "message_body": self.message_body}
