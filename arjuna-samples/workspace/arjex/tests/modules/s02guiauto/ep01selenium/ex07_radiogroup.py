from arjuna.tpi import Arjuna
from arjuna.tpi.markup import *
from arjuna.tpi.guiauto import With

from .wp import WPLoginLogout


@test_function
def test(my):
    automator = Arjuna.create_gui_automator()

    WPLoginLogout.login(automator)

    automator.Element(With.link_text("Settings")).click()

    data_format = automator.RadioGroup(With.name("date_format"))
    print(data_format.has_value_selected("Y-m-d"))
    print(data_format.has_index_selected(1))
    print(data_format.get_first_selected_option_value())
    data_format.select_by_value(r"\c\u\s\t\o\m")
    data_format.select_by_index(2)
    
    WPLoginLogout.logout(automator)
