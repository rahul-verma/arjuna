from commons import *


config = init_arjuna().config

print(config.get_user_option_value("wp.app.url").as_str())
print(config.get_user_option_value("wp.login.url").as_str())
print(config.get_user_option_value("wp.logout.url").as_str())
