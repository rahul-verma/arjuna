from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.guiauto.helpers import With
from arjuna.revised.tpi.guiauto.helpers import Screen

from .wp_login_logout import *

Arjuna.init()
# Default Gui automation engine is Selenium
automator = Arjuna.create_gui_automator(Arjuna.get_central_config())

login(automator)

automator.Element(With.link_text("Posts")).click()
automator.Element(With.link_text("Categories")).click()

checkboxes = automator.MultiElement(With.name("delete_tags[]"))
check_boxex.at_index(0).uncheck()
check_boxex.at_index(0).check()
check_boxex.at_index(0).check()
check_boxex.at_index(1).uncheck()

check_boxex.first.uncheck()
check_boxex.last.uncheck()
check_boxex.random.uncheck()

logout(automator)