import logging
import yaml
from addict import Dict


# class DictNoDefault(Dict):
#     def __missing__(self, key):
#         # raise KeyError(key)
#         return None


def load_yaml(file_path):
    file = open(file_path, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()

    return Dict(yaml.load(file_data, Loader=yaml.CLoader))
