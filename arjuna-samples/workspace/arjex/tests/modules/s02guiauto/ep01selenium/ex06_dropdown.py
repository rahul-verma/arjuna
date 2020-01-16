from arjuna.tpi import Arjuna
from arjuna.tpi.markup import *
from arjuna.tpi.guiauto import With

from .wp import WPLoginLogout


@test_function
def test(my):
    automator = Arjuna.create_gui_automator()

    WPLoginLogout.login(automator)
    automator.element(With.link_text("Settings")).click()

    role_select = automator.DropDown(With.id("default_role"))
    print(role_select.has_visible_text_selected("Subscriber"))
    print(role_select.has_value_selected("subscriber"))
    print(role_select.has_index_selected(2))
    print(role_select.get_first_selected_option_text())
    role_select.select_by_value("editor")
    role_select.select_by_visible_text("Subscriber")
    role_select.select_by_index(4)
    
    WPLoginLogout.logout(automator)
