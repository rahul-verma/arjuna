from commons import *
from arjuna.tpi.guiauto.helpers import With

init_arjuna()

automator = launch_automator()
go_to_wp_home(automator)

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