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

import yaml
import os

cfgdir: str = ""


class ConfigManager:
    _instance = None
    _register: dict = {}
    _default: dict = {}

    def __new__(cls, *args, **kwargs):
        cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __getitem__(self, item):
        if item in self._register:
            return self._register.get(item)
        else:
            return self._default.get(item)

    def set(self, attr: str, default=None):
        self._default[attr] = default

    def read_default(self, path: str):
        if not self._default:
            self._default = self.__load(path)

    def load_config(self, path: str):
        if not self._register:
            self._register = self.__load(path)

    def __load(self, path: str):
        if path.endswith(".yml") or path.endswith(".yaml"):
            with open(path, "r", encoding="utf-8") as f:
                return yaml.load(f.read(), Loader=yaml.FullLoader)


def config(cfg: str):
    cfgfile = "./config/system/config.yaml"
    cfg_manager = ConfigManager()
    cfg_manager.read_default(cfgfile)
    if cfg:
        cfg_manager.load_config(cfg)
    return cfg_manager


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
