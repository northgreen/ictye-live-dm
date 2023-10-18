import logging

def logging_setup(config):

    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s,%(name)s] %(levelname)s : %(message)s")
