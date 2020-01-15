from commons import *
from arjuna.tpi.guiauto.helpers import With, Screen

init_arjuna()

automator = launch_automator()
go_to_wp_home(automator)

user, pwd = automator.config.get_user_option_value("wp.users.admin").split_as_str_list()

# Login
automator.Element(With.id("user_login")).set_text(user)
automator.Element(With.id("user_pass")).set_text(pwd)
automator.Element(With.id("wp-submit")).click()

automator.Element(With.class_name("welcome-view-site")).wait_until_visible()

# Logout
url = automator.config.get_user_option_value("wp.logout.url").as_str()
automator.browser.go_to_url(url)

automator.Element(With.link_ptext("log out")).click()
message = automator.Element(With.ptext("logged out")).wait_until_visible()

automator.quit()