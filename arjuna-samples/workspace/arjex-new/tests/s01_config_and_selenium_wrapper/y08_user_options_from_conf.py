from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.enums import ArjunaOption

config = Arjuna.get_central_config()

print(config.get_user_option_value("wp.app.url").as_str())
print(config.get_user_option_value("wp.login.url").as_str())
print(config.get_user_option_value("wp.logout.url").as_str())
