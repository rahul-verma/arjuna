from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.guiauto.helpers import With

Arjuna.init()
# Default Gui automation engine is Selenium
automator = Arjuna.create_gui_automator(Arjuna.get_central_config())

url = automator.config.get_user_option_value("wp.login.url").as_str()
automator.browser.go_to_url(url)

# Based on any attribute e.g. for
element = automator.Element(With.css_selector("*[for = 'user_login']"))
element.identify()
print(element.source.content.root)

# Based on partial content of an attribute
element = automator.Element(With.css_selector("*[for *= '_login']"))
element.identify()
print(element.source.content.root)

# Based on element type
element = automator.Element(With.css_selector("*[type ='password']"))
element.identify()
print(element.source.content.root)

# Based on compound classes
element = automator.Element(With.css_selector(".button.button-large"))
element.identify()
print(element.source.content.root)

automator.quit()