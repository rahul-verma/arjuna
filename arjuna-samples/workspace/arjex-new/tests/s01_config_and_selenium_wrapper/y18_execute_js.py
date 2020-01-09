from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.guiauto.helpers import With
from arjuna.revised.tpi.guiauto.helpers import Screen

from .wp_login_logout import *

Arjuna.init()
# Default Gui automation engine is Selenium
automator = Arjuna.create_gui_automator(Arjuna.get_central_config())

login(automator)

automator.execute_script("document.getElementsByClassName('welcome-view-site')[0].click();")
automator.Element(With.link_text("Site Admin")).wait_until_clickable()

logout(automator)