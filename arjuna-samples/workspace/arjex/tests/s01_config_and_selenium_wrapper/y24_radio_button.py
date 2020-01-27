from arjuna.tpi import Arjuna
from arjuna.interact.gui.helpers import With

from commons import *

init_arjuna()
automator = launch_automator()
login(automator)

automator.element(With.link_text("Settings")).click()

date_format = automator.radio_group(With.name("date_format"))
print(date_format.has_value_selected("Y-m-d"))
print(date_format.has_index_selected(1))
print(date_format.first_selected_option_value)
date_format.select_value(r"\c\u\s\t\o\m")
date_format.select_index(2)

logout(automator)