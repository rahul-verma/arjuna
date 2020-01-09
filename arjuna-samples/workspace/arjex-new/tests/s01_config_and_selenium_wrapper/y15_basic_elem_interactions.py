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
user_field = automator.Element(With.id("user_login"))
user_field.identify()
user_field.wait_until_clickable()
user_field.set_text(user)

pwd_field = automator.Element(With.id("user_pass"))
pwd_field.identify()
pwd_field.wait_until_clickable()
pwd_field.set_text(pwd)

submit = automator.Element(With.id("wp-submit"))
submit.identify()
submit.wait_until_clickable()
submit.click()

automator.Element(With.class_name("welcome-view-site")).wait_until_visible()

# Logout
url = automator.config.get_user_option_value("wp.logout.url").as_str()
automator.browser.go_to_url(url)

confirmation = automator.Element(With.partial_link_text("log out"))
confirmation.identify()
confirmation.wait_until_clickable()
confirmation.click()

message = automator.Element(With.partial_text("logged out"))
message.identify()
message.wait_until_visible()

automator.quit()