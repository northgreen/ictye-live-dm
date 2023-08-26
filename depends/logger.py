import logging
import configs

def logging_setup():
    config = configs.config()

    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s,%(name)s] %(levelname)s : %(message)s")