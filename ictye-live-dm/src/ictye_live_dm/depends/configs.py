import os

import yaml

cfgdir: str = ""


class ConfigManager:
    _instance = None
    _register: dict = {}
    _default: dict = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
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
