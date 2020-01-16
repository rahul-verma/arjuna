from commons import *
from arjuna.tpi.guiauto.helpers import With, Screen

init_arjuna()

automator = launch_automator()
go_to_wp_home(automator)

user, pwd = automator.config.get_user_option_value("wp.users.admin").split_as_str_list()

# Login
user_field = automator.element(With.id("user_login"))
user_field.identify()
user_field.wait_until_clickable()
user_field.set_text(user)

pwd_field = automator.element(With.id("user_pass"))
pwd_field.identify()
pwd_field.wait_until_clickable()
pwd_field.set_text(pwd)

submit = automator.element(With.id("wp-submit"))
submit.identify()
submit.wait_until_clickable()
submit.click()

automator.element(With.class_name("welcome-view-site")).wait_until_visible()

# Logout
url = automator.config.get_user_option_value("wp.logout.url").as_str()
automator.browser.go_to_url(url)

confirmation = automator.element(With.link_ptext("log out"))
confirmation.identify()
confirmation.wait_until_clickable()
confirmation.click()

message = automator.element(With.ptext("logged out"))
message.identify()
message.wait_until_visible()

automator.quit()