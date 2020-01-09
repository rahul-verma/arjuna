from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.guiauto.helpers import With

Arjuna.init()
# Default Gui automation engine is Selenium
automator = Arjuna.create_gui_automator(Arjuna.get_central_config())

url = automator.config.get_user_option_value("wp.login.url").as_str()
automator.browser.go_to_url(url)

# The following code is for user name field.
# Html of user name: <input type="text" name="log" id="user_login" class="input" value="" size="20">
element = automator.Element(With.id("user_login"))
element.identify()
print(element.source.content.root)

element = automator.Element(With.name("log"))
element.identify()
print(element.source.content.root)

element = automator.Element(With.class_name("input"))
element.identify()
print(element.source.content.root)

element = automator.Element(With.tag_name("input"))
element.identify()
print(element.source.content.root)

# The following options are for 
# Html of link: <a href="http://192.168.56.103/wp-login.php?action=lostpassword" title="Password Lost and Found">Lost your password?</a>
element = automator.Element(With.link_text("Lost your password?"))
element.identify()
print(element.source.content.root())

element = automator.Element(With.partial_link_text("password"))
element.identify()
print(element.source.content.root())

automator.quit()
