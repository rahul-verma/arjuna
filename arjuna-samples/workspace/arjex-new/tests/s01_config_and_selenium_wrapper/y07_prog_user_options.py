from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.enums import ArjunaOption

context = Arjuna.init()
cb = context.config_builder
cb.user_option("my.custom.name", 12)
cb.build()

config = context.get_config()

print(config.get_user_option_value("my.custom.name").as_int())
print(config.get_user_option_value("my_CUSTOM_name").as_int())
