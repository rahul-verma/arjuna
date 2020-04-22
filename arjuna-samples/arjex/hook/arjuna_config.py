from arjuna import *


def register_configs(configurator: Configurator):
    cb = configurator.builder(base_config="data1_tenv1")
    cb.test_value = 123
    cb.register(config_name="hook_conf")

    

