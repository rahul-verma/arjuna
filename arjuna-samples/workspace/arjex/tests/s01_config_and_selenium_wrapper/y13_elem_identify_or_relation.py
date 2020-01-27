from arjuna import *
from commons import *

init_arjuna()
wordpress = create_wordpress_app()

# Two identifiers. Only first one would be tried as it succeeds.
element = wordpress.ui.element(With.id("user_login"), With.name("log"))
element.identify()
print(element.source.content.root)

# Two identifiers. First invalid, second valid. Hence it succeeds by using second With construct
# Identification max wait time is for all With constructs clubbed together.
element = wordpress.ui.element(With.id("INVALID"), With.name("log"))
element.identify()
print(element.source.content.root)

wordpress.quit()