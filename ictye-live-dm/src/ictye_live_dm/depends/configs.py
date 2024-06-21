import os

import yaml

from . import config_registrar

cfgdir: str = ""


def regist_default(_config_registrar: config_registrar.ConfigRegistrar):
    """
    注册默认配置
    """
    _config_registrar.register("port", default=8083)
    _config_registrar.register("host", default="127.0.0.1")
    _config_registrar.register("web", default={"index": "./web/living room dm.html"})
    _config_registrar.register("GUI", default=False)
    _config_registrar.register("plugins", default={})
    _config_registrar.register("debug", default=False)
    _config_registrar.register("loglevel", default="INFO", option=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "FATAL"])
    _config_registrar.register("logfile", default={"open": True, "name": "latestlog"})
    _config_registrar.register("dev", default=False)
    _config_registrar.register("use_local_plugin", default=False)


class ConfigManager:
    _instance = None
    _register: config_registrar.ConfigRegistrar = config_registrar.ConfigRegistrar()
    _default: dict = {}
    _inited = False

    def __init__(self):
        if not self._inited:
            regist_default(self._register)
        self._inited = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __getitem__(self, item):
        return self._register[item]

    def __setitem__(self, key, value):
        self._register[key] = value

    def set(self, attr: str, default=None):
        self._default[attr] = default

    def read_default(self, path: str):
        default = self.__load(path)
        for k, v in default.items():
            self._register.set(k, v)

    def load_config(self, path: str):
        if not self._register:
            self._register = self.__load(path)

    def __load(self, path: str):
        if path.endswith(".yml") or path.endswith(".yaml"):
            with open(path, "r", encoding="utf-8") as f:
                return yaml.load(f.read(), Loader=yaml.FullLoader)


def set_config(config_family: str, config: dict) -> bool:
    """
    设置插件的配置
    """
    try:
        with open(f"./config/plugin/{config_family}/config.yaml", "w", encoding="utf_8") as f:
            yaml.dump(data=config, stream=f, allow_unicode=True)
    except Exception as e:
        print(str(e))
        return False
    finally:
        return True


def read_config(config_family: str) -> dict:
    """
    读取插件的配置
    """
    configs = {}
    if os.path.exists(f"./config/plugin/{config_family}/config.yaml"):
        with open(f"./config/plugin/{config_family}/config.yaml", "r", encoding="utf_8") as f:
            configs = yaml.load(f.read(), Loader=yaml.FullLoader)
            return configs
    else:
        os.makedirs(os.path.dirname(f"./config/plugin/{config_family}/config.yaml"), exist_ok=True)
        with open(f"./config/plugin/{config_family}/config.yaml", 'w+') as f:
            f.write(f"# config for {config_family}")
        return configs
