class connect_ok:
    code = 200
    msg = "connect ok"

    def to_dict(self):
        return {"code": self.code, "msg": self.msg}


class msg:
    def __init__(self, msg, body):
        self.msg = msg
        self.body = body

    def to_dict(self):
        return {"msg": self.msg, "body": self.body}


class dm:
    def __init__(self, msg, who):
        self.msg = msg
        self.who = who

    def to_dict(self):
        return {"msg": self.msg,
                "who": self.who}


class info:
    def __init__(self, msg, who, pic_url, pic_style):
        self.msg = msg
        self.who = who
        self.pic_url = pic_url
        self.pic_style = pic_style

    def to_dict(self):
        return {"msg": self.msg,
                "who": self.who,
                "pic url": self.pic_url,
                "pic style": self.pic_style}


class socket_responce:
    def __init__(self, config):
        self.code = 200
        self.local = "ws://{}:{}".format(config["host"], config["websocket"]["port"])

    def to_dict(self):
        return {"code": self.code,
                "local": self.local}
