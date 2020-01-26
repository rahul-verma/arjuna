from commons import *
from arjuna.tpi.guiauto.helpers import With
from arjuna.tpi.guiauto import WebApp

init_arjuna()
wordpress = create_wordpress_app()

user, pwd = wordpress.config.get_user_option_value("wp.users.admin").split_as_str_list()

# Login
wordpress.ui.element(With.id("user_login")).text = user
wordpress.ui.element(With.id("user_pass")).text = pwd
wordpress.ui.element(With.id("wp-submit")).click()

wordpress.ui.element(With.class_name("welcome-view-site")).wait_until_visible()

# Logout
url = wordpress.ui.config.get_user_option_value("wp.logout.url").as_str()
wordpress.ui.browser.go_to_url(url)

wordpress.ui.element(With.link_ptext("log out")).click()
message = wordpress.ui.element(With.ptext("logged out")).wait_until_visible()

wordpress.quit()