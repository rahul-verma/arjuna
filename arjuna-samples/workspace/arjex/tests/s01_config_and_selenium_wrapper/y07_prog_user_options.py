from commons import *
from arjuna.tpi.enums import ArjunaOption

context = init_arjuna()
cc = context.config_creator
cc.user_option("my.custom.name", 12)
cc.register()

config = context.config

print(config.get_user_option_value("my.custom.name").as_int())
print(config.get_user_option_value("my_CUSTOM_name").as_int())
