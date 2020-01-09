from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.guiauto.helpers import With
from arjuna.revised.tpi.guiauto.helpers import Screen

Arjuna.init()
# Default Gui automation engine is Selenium
automator = Arjuna.create_gui_automator(Arjuna.get_central_config())

url = automator.config.get_user_option_value("wp.login.url").as_str()
automator.browser.go_to_url(url)

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