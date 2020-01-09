from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.guiauto.helpers import With
from arjuna.revised.tpi.guiauto.helpers import Screen

Arjuna.init()
# Default Gui automation engine is Selenium
automator = Arjuna.create_gui_automator(Arjuna.get_central_config())

url = automator.config.get_user_option_value("wp.login.url").as_str()
automator.browser.go_to_url(url)

user, pwd = automator.config.get_user_option_value("wp.users.admin").split()

# Login
automator.Element(With.id("user_login")).set_text(user)
automator.Element(With.id("user_pass")).set_text(pwd)
automator.Element(With.id("wp-submit")).click()
automator.Element(With.class_name("welcome-view-site")).wait_until_visible()

# Logout
url = automator.config.get_user_option_value("wp.logout.url").as_str()
automator.browser.go_to_url(url)

automator.Element(With.partial_link_text("log out")).click()
automator.Element(With.partial_text("logged out")).wait_until_visible()

automator.quit()