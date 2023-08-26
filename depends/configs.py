import yaml


def config():
    with open("./depends/config.yaml", "r", encoding="utf-8") as f:
        configs = yaml.load(f.read(), Loader=yaml.FullLoader)
    if configs["debug"] == 1:
        print(f"log:already reading config file:    {configs}\n")
    return configs
