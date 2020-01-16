from arjuna.tpi import Arjuna
from arjuna.tpi.guiauto.helpers import With

from commons import *

init_arjuna()
automator = launch_automator()
login(automator)

automator.element(With.link_text("Posts")).click()
automator.element(With.link_text("Categories")).click()

check_boxes = automator.multi_element(With.name("delete_tags[]"))
check_boxes.at_index(0).uncheck()
check_boxes.at_index(0).check()
check_boxes.at_index(0).check()
check_boxes.at_index(1).uncheck()

check_boxes.first.uncheck()
check_boxes.last.uncheck()
check_boxes.random.uncheck()

logout(automator)