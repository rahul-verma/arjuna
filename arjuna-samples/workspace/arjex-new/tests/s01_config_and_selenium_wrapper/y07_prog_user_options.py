from commons import *
from arjuna.tpi.enums import ArjunaOption

context = init_arjuna()
cb = context.ConfigBuilder()
cb.user_option("my.custom.name", 12)
cb.build()

config = context.config

print(config.get_user_option_value("my.custom.name").as_int())
print(config.get_user_option_value("my_CUSTOM_name").as_int())
