from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.guiauto.helpers import With

Arjuna.init()
# Default Gui automation engine is Selenium
automator = Arjuna.create_gui_automator(Arjuna.get_central_config())

url = automator.config.get_user_option_value("wp.login.url").as_str()
automator.browser.go_to_url(url)

# Based on Text
element = automator.Element(With.xpath("//*[text() = 'Lost your password?']"))
element.identify()
print(element.source.content.root)

# Based on partial text
element = automator.Element(With.xpath("//*[contains(text(), 'Lost')]"))
element.identify()
print(element.source.content.root)

# Based on Title
element = automator.Element(With.xpath("//*[@title = 'Password Lost and Found']"))
element.identify()
print(element.source.content.root)

# Based on Value
element = automator.Element(With.xpath("//*[@value = 'Log In']"))
element.identify()
print(element.source.content.root)

# Based on any attribute e.g. for
element = automator.Element(With.xpath("//*[@for = 'user_login']"))
element.identify()
print(element.source.content.root())

# Based on partial content of an attribute
element = automator.Element(With.xpath("//*[contains(@for, '_login')]"))
element.identify()
print(element.source.content.root())

# Based on element type
element = automator.Element(With.xpath("//*[@type ='password']"))
element.identify()
print(element.source.content.root())

automator.quit()