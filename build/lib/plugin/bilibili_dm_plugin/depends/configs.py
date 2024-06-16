import yaml


def config() -> dict:
    with open("./config/system/config.yaml", "r", encoding="utf-8") as f:
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
    with open(f"./config/plugin/{config_family}/config.yaml", "r", encoding="utf_8") as f:
        configs = yaml.load(f.read(), Loader=yaml.FullLoader)
    return configs

