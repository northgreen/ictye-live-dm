import yaml


def config():
    with open("./config/system/config.yaml", "r", encoding="utf-8") as f:
        configs = yaml.load(f.read(), Loader=yaml.FullLoader)
    if configs["debug"] == 1:
        print(f"log:already reading config file: {configs}\n")
    return configs


def set_config(config_family: str, config: dict):
    with open(f"./config/plugin/{config_family}/config.yaml", "w", encoding="utf_8") as f:
        yaml.dump(data=config, stream=f, allow_unicode=True)
