from commons import *
from arjuna.tpi.guiauto.helpers import With, Screen

init_arjuna()

automator = launch_automator()
go_to_wp_home(automator)

# Two identifiers. Only first one would be tried as it succeeds.
element = automator.Element(With.id("user_login"), With.name("log"))
element.identify()
print(element.source.content.root)

# Two identifiers. First invalid, second valid. Hence it succeeds by using second With construct
# Identification max wait time is for all With constructs clubbed together.
element = automator.Element(With.id("INVALID"), With.name("log"))
element.identify()
print(element.source.content.root)

automator.quit()