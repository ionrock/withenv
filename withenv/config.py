import os
import yaml


CONFIG_FILE = '.werc'


def find_config_file(start=None, filename=CONFIG_FILE):
    start = start or os.getcwd()
    conf = os.path.join(start, filename)
    if os.path.exists(conf):
        return conf

    if start == os.path.abspath(os.sep):
        return None

    parent = os.path.normpath(os.path.abspath(os.path.join(start, '..')))
    return find_config_file(parent)


def load_config_file():
    config_path = find_config_file()
    if not config_path:
        return []
    return [('alias', config_path)]
