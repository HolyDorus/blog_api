from os import getenv

from . import configs_list

config_class_name = getenv('APP_CONFIG_CLASS')
settings = getattr(configs_list, config_class_name)
