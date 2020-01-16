from commons import *
from arjuna.tpi.guiauto.helpers import With

init_arjuna()

automator = launch_automator()
go_to_wp_home(automator)

# Based on Text
element = automator.element(With.xpath("//*[text() = 'Lost your password?']"))
element.identify()
print(element.source.content.root)

# Based on partial text
element = automator.element(With.xpath("//*[contains(text(), 'Lost')]"))
element.identify()
print(element.source.content.root)

# Based on Title
element = automator.element(With.xpath("//*[@title = 'Password Lost and Found']"))
element.identify()
print(element.source.content.root)

# Based on Value
element = automator.element(With.xpath("//*[@value = 'Log In']"))
element.identify()
print(element.source.content.root)

# Based on any attribute e.g. for
element = automator.element(With.xpath("//*[@for = 'user_login']"))
element.identify()
print(element.source.content.root)

# Based on partial content of an attribute
element = automator.element(With.xpath("//*[contains(@for, '_login')]"))
element.identify()
print(element.source.content.root)

# Based on element type
element = automator.element(With.xpath("//*[@type ='password']"))
element.identify()
print(element.source.content.root)

automator.quit()