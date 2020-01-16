from commons import *
from arjuna.tpi.guiauto.helpers import With, Screen

init_arjuna()

automator = launch_automator()
go_to_wp_home(automator)

user, pwd = automator.config.get_user_option_value("wp.users.admin").split_as_str_list()

# Login
automator.element(With.id("user_login")).set_text(user)
automator.element(With.id("user_pass")).set_text(pwd)
automator.element(With.id("wp-submit")).click()

automator.element(With.class_name("welcome-view-site")).wait_until_visible()

# Logout
url = automator.config.get_user_option_value("wp.logout.url").as_str()
automator.browser.go_to_url(url)

automator.element(With.link_ptext("log out")).click()
message = automator.element(With.ptext("logged out")).wait_until_visible()

automator.quit()