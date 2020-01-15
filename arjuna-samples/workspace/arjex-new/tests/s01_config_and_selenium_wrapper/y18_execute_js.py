from arjuna.tpi import Arjuna
from arjuna.tpi.guiauto.helpers import With

from commons import *

init_arjuna()
automator = launch_automator()
login(automator)

automator.execute_javascript("document.getElementsByClassName('welcome-view-site')[0].click();")
automator.Element(With.link_text("Site Admin")).wait_until_clickable()

logout(automator)