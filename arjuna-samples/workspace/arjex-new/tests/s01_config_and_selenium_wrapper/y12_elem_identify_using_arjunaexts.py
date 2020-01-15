from commons import *
from arjuna.tpi.guiauto.helpers import With, Screen

init_arjuna()

automator = launch_automator()
go_to_wp_home(automator)

# Based on Text
element = automator.Element(With.text("Lost your password?"))
element.identify()
print(element.source.content.root)

# Based on partial text
element = automator.Element(With.ptext("Lost"))
element.identify()
print(element.source.content.root)

# Based on Title
element = automator.Element(With.title("Password Lost and Found"))
element.identify()
print(element.source.content.root)

# Based on Value
element = automator.Element(With.value("Log In"))
element.identify()
print(element.source.content.root)

# Based on any attribute e.g. for
element = automator.Element(With.attr_value("[for][user_login]"))
element.identify()
print(element.source.content.root)

# Based on partial content of an attribute
element = automator.Element(With.attr_pvalue("[for][_login]"))
element.identify()
print(element.source.content.root)

# Based on element type
element = automator.Element(With.type("password"))
element.identify()
print(element.source.content.root)

# Based on compound classes
element = automator.Element(With.compound_class("button button-large"))
element.identify()
print(element.source.content.root)

# Based on class names
element = automator.Element(With.class_names("button", "button-large"))
element.identify()
print(element.source.content.root)

# Based on Point (location in terms of X,Y co-ordinates)
element = automator.Element(With.point(Screen.xy(1043, 458)))
element.identify()
print(element.source.content.root)

# With Javascript
element = automator.Element(With.javascript("return document.getElementById('wp-submit')"))
element.identify()
print(element.source.content.root)
# To understand this further look at the javascript situations code

automator.quit()