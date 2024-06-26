import yaml
import os

cfgdir: str = ""


def config(cfg: str) -> dict:
    cfgdir = cfg
    if cfg:
        cfgfile = cfg
    else:
        cfgfile = "./config/system/config.yaml"
    with open(cfgfile, "r", encoding="utf-8") as f:
        configs = yaml.load(f.read(), Loader=yaml.FullLoader)
    if configs["debug"] == 1:
        print(f"log:already reading config file: {configs}\n")
    return configs


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
