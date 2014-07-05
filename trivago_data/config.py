# -*- encoding: utf-8 -*-

import os
import yaml
import logging
import logging.config

CONFIG = yaml.load(open("config.yaml").read())

def setup_logging():
    logging.config.dictConfig(CONFIG["logging"])

activate_logging = setup_logging()

class Paths(object):

    def __init__(self):
        self.base = base = CONFIG["paths"]["data"]
        for name in CONFIG["paths"]["files"]:
            path = os.path.join(base, CONFIG["paths"]["files"][name])
            setattr(self, name, path)

    def has_label(self, name):
        return "train" in name

paths = Paths()
PARTS = CONFIG["parts"]
