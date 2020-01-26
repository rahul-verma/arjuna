from commons import *
from arjuna.tpi.guiauto.helpers import With
from arjuna.tpi.guiauto import WebApp

init_arjuna()
wordpress = create_wordpress_app()

# Based on any attribute e.g. for
element = wordpress.ui.element(With.css_selector("*[for = 'user_login']"))
print(element.source.content.root)

# Based on partial content of an attribute
element = wordpress.ui.element(With.css_selector("*[for *= '_login']"))
print(element.source.content.root)

# Based on element type
element = wordpress.ui.element(With.css_selector("*[type ='password']"))
print(element.source.content.root)

# Based on compound classes
element = wordpress.ui.element(With.css_selector(".button.button-large"))
print(element.source.content.root)

wordpress.quit()