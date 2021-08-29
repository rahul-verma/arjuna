from arjuna import *


def register_ref_confs(configurator: Configurator):
    cb = configurator.builder(base_config="data1_env1")
    cb.test_value = 123
    cb.register(config_name="hook_conf")

    

