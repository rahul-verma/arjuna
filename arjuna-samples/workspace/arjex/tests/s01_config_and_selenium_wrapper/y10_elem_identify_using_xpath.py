from commons import *
from arjuna import *

init_arjuna()
wordpress = create_wordpress_app()

# Based on Text
element = wordpress.ui.element(With.xpath("//*[text() = 'Lost your password?']"))
print(element.source.content.root)

# Based on partial text
element = wordpress.ui.element(With.xpath("//*[contains(text(), 'Lost')]"))
print(element.source.content.root)

# Based on Title
element = wordpress.ui.element(With.xpath("//*[@title = 'Password Lost and Found']"))
print(element.source.content.root)

# Based on Value
element = wordpress.ui.element(With.xpath("//*[@value = 'Log In']"))
print(element.source.content.root)

# Based on any attribute e.g. for
element = wordpress.ui.element(With.xpath("//*[@for = 'user_login']"))
print(element.source.content.root)

# Based on partial content of an attribute
element = wordpress.ui.element(With.xpath("//*[contains(@for, '_login')]"))
print(element.source.content.root)

# Based on element type
element = wordpress.ui.element(With.xpath("//*[@type ='password']"))
print(element.source.content.root)

wordpress.quit()