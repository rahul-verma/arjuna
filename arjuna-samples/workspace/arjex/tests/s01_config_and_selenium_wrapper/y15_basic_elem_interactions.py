from commons import *
from arjuna.tpi.guiauto.helpers import With
from arjuna.tpi.guiauto import WebApp

init_arjuna()
wordpress = create_wordpress_app()

user, pwd = wordpress.config.get_user_option_value("wp.users.admin").split_as_str_list()

# Login
user_field = wordpress.ui.element(With.id("user_login"))
user_field.wait_until_clickable()
user_field.text = user

pwd_field = wordpress.ui.element(With.id("user_pass"))
pwd_field.wait_until_clickable()
pwd_field.text = pwd

submit = wordpress.ui.element(With.id("wp-submit"))
submit.wait_until_clickable()
submit.click()

wordpress.ui.element(With.class_name("welcome-view-site")).wait_until_visible()

# Logout
url = wordpress.ui.config.get_user_option_value("wp.logout.url").as_str()
wordpress.ui.browser.go_to_url(url)

confirmation = wordpress.ui.element(With.link_ptext("log out"))
confirmation.wait_until_clickable()
confirmation.click()

message = wordpress.ui.element(With.ptext("logged out"))
message.wait_until_visible()

wordpress.quit()